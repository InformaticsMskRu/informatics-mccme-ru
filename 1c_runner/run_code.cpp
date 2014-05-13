#include "soapServiceSoapBindingProxy.h"
#include "ServiceSoapBinding.nsmap"
#include <iostream>
#include <map>
#include <fstream>
#include <sstream>
#include <thread>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#define BOOST_NO_CXX11_SCOPED_ENUMS
#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/locale.hpp>
#include <boost/uuid/uuid.hpp>            // uuid class
#include <boost/uuid/uuid_io.hpp>            // uuid class
#include <boost/uuid/uuid_generators.hpp> // generators

using namespace std;
using namespace boost::filesystem;
using namespace boost::locale;

volatile bool flag;

void handler(int sig) 
{
    flag = true;
}

const int SUCCESS = 0;
const int FAIL = -1;
const int RUNNING = 1;

class ServiceClient 
{
    ServiceSoapBindingProxy service;
    const char *login;
    const char *password;

public:
    ServiceClient(const char *login, const char *password, const char *endpoint):
        login(login), password(password)
    {
        service.soap_endpoint = endpoint;    
    }

    void setAuth() 
    {
        service.userid = login;
        service.passwd = password;
    }

    string stopCode(const string& id) 
    {
        setAuth();
        _ns1__Stop stop;
        _ns1__StopResponse responseStop;

        stop.ID = id;

        int res = service.Stop(&stop, &responseStop);
        if (res != 0) {
            cerr << "Service stop " << res << endl;
            throw res;
        }
        return responseStop.return_;       
    }

    string startCode(const string& uuid, const string& code) 
    {
        setAuth();
        _ns1__Start start;
        _ns1__StartResponse response;
//        start.Code = code;
        start.Uuid = uuid;
    
        int res = service.Start(&start, &response);
        if (res != 0) {
            throw res;
        }
        return response.return_;
    }

    int getStatus(const string& id) 
    {
        setAuth();
         _ns1__Status status;
        _ns1__StatusResponse responseStatus;
        status.ID = id;
        
        int attempts = 10;
        while (attempts) {
            setAuth();
            int res = service.Status(&status, &responseStatus);
            if (res != 0) {
                cerr << "status attempt" << res << endl;
             } else {
                break;
            }
            --attempts;
            if (!attempts) {
                cerr << "status error" << endl;
            }
        }

        if (responseStatus.return_ == "Job failed") {
            return FAIL;
        }

        if (responseStatus.return_ == "Job is completed") {
            return SUCCESS;
        }
        return RUNNING;
    }

    int runCode(const string& uuid, const string& code, int tl_ms) 
    {
        flag = false;
        string id = startCode(uuid, code);
        cerr << "task id " << id << endl;
        while (true) 
        {
            int status = getStatus(id);
            if (status != 1) {
                if (status != 0) {
                    cerr << "RE " << status << endl;
                }
                cerr << stopCode(id) << endl;
                return status;
            }

            if (flag) // RTL
            {
                cerr << "RTL" << endl;
                cerr << stopCode(id) << endl;
                return 239;
            }

            tl_ms -= 100;
            chrono::milliseconds dura(100);
            this_thread::sleep_for(dura);
            cerr << tl_ms << endl;
            if (tl_ms < 0) {
                cerr << "TL" << endl;
                cerr << stopCode(id) << endl;
                return 238;
            }
        }
    }

};

std::pair<std::string, std::string> fix_string(const string& str) {
    std::string status = "";
    try {
        conv::utf_to_utf<wchar_t>(str, conv::stop);
        return make_pair(str, string("utf8"));
    } catch (...) {
        status += "not utf8";
    }

    try {
        return make_pair(conv::to_utf<char>(str, "cp1251", conv::stop), status + ", cp1251");
    } catch (...) {
        status += ", not cp1251";
    }
    return make_pair(str, status);
}

std::pair<std::string, bool> fix_bom(const std::string& str) 
{
    std::string res = str;
    if (str.size() >= 3) {
        if (str[0] == '\xEF' && str[1] == '\xBB' && str[2] == '\xBF') {
            return make_pair(string(str.begin() + 3, str.end()), true);
        }
    }
    return make_pair(str, false);
}

std::map<std::string, std::string> parse_env(char *envp[]) 
{
	std::map<std::string, std::string> env;
    int i = 0;
    while (envp[i]) {
        char *pos = strchr(envp[i], '=');
        *pos = '\0';
        ++pos;
        env[string(envp[i])] = string(pos);
        ++i;
    }

    if (!env.count("SUSER")) {
    	env["SUSER"] = "test";
    }
    if (!env.count("SPASS")) {
    	env["SPASS"] = "";
    }
    if (!env.count("URL")) {
    	env["URL"] = "http://192.168.56.11/test/ws/service.1cws";
    }
    if (!env.count("WORKDIR")) {
    	env["WORKDIR"] = "/var/1c_workdir/";
    }
    if (!env.count("INPUT_FILENAME")) {
    	env["INPUT_FILENAME"] = "input.txt";
    }
    if (!env.count("OUTPUT_FILENAME")) {
    	env["OUTPUT_FILENAME"] = "output.txt";
    }
    if (!env.count("TIMELIMIT")) {
    	env["TIMELIMIT"] = "2000";
    }

    return env;
}

int main(int argc, char* argv[], char *envp[])
{
    signal(SIGINT, handler);
    if (argc < 2) {
        std::cerr << "fail: source file must be specified" << std::endl;
        exit(1);
    }

    std::map<std::string, std::string> env = parse_env(envp);

    ServiceClient client(env["SUSER"].c_str(), env["SPASS"].c_str(), env["URL"].c_str());
    stringstream ss;
    boost::uuids::uuid uuid_u = boost::uuids::random_generator()();
    ss << uuid_u;
    std::string uuid = ss.str();
    std::cerr << "note: testing uuid " << uuid << std::endl;

    path target_dir = path(env["WORKDIR"]);
    target_dir += string(uuid); 
    path input_path = target_dir;
    input_path += string("/") + env["INPUT_FILENAME"];
    create_directories(target_dir);
    permissions(target_dir, add_perms | perms(0666));
    copy_file(env["INPUT_FILENAME"], input_path);

    ifstream source(argv[1]);
    string src = string(std::istreambuf_iterator<char>(source), 
               std::istreambuf_iterator<char>());
    auto res_bom = fix_bom(src);
    if (res_bom.second) {
        std::cerr << "note: remove BOM from source" << std::endl;
    }
    auto res = fix_string(std::move(res_bom.first));
    cerr << "note: encoding convertion - " << res.second << std::endl;

   	path source_file = target_dir;
   	source_file += string("/source.txt");

   	{
        ofstream res_file(source_file.string());
        res_file << res.first;
   	}

    int ret_code = client.runCode(uuid, res.first, atoi(env["TIMELIMIT"].c_str()));
    if (ret_code == 0) { // copy output.txt to ejudge
    	path output_file = target_dir;
    	output_file += string("/") + env["OUTPUT_FILENAME"];
        ifstream user_out(output_file.string());
        if (user_out) {
            string output = string(std::istreambuf_iterator<char>(user_out), std::istreambuf_iterator<char>());

            auto res = fix_bom(output);
            if (res.second) {
                std::cerr << "note: BOM in output file" << std::endl;
            }
            ofstream res_file(env["OUTPUT_FILENAME"]);
            res_file << res.first;
        }
    }

    for_each(recursive_directory_iterator(target_dir),
             recursive_directory_iterator(), 
             [] (const directory_entry& d) {
                 std::cerr << "note: target content: " << d.path() << std::endl;
             });
    remove_all(target_dir);

    return ret_code;
}

