import os
from serve_internal import EjudgeContestCfg
from datetime import datetime
import shutil
import random
random.seed()

#used to mark backup for undo purpose
version_stamp = str(random.randint(100000000,999999999))

HOME_JUDGES = '/home/judges/'
SPECIAL = [14, 1651, 1887, 1850, 1851] #contests with special configs

def get_contest_path(number):
    return HOME_JUDGES + '0'*(6-len(str(number))) + str(number)

def get_contest_path_conf(number):
    return get_contest_path(number) + '/conf/'


def all_contests():
    ''' Generates all contest_id '''
    xmllist = os.listdir(os.path.join(HOME_JUDGES, 'data/contests/'))
    for filename in xmllist:
        if filename.endswith('.xml'):
            contest_id = filename.split('.')[0]
            yield contest_id

def regular_contests():
    ''' Generates all contest_id '''
    xmllist = os.listdir(os.path.join(HOME_JUDGES, 'data/contests/'))
    for filename in xmllist:
        if filename.endswith('.xml'):
            contest_id = filename.split('.')[0]
            try:
                if not int(contest_id) in SPECIAL:
                    yield contest_id
            except ValueError:
                pass

def edit_serve_cfg(path = None, contests = None,
                   function = None):
    '''edit one or more serve.cfg files

    path - path to serve.cfg file, for example /home/judges/000001/conf/
          if set, contests parameter is not used

    contests - used if path is None.
               Number of contest (for example, 14) or
               list of numbers (for example [14, 789, 32]) or
               string 'all' to edit all contests configs or
               string 'regular' to edit all contests except SPECIAL
               (SPECIALL contests are contests with specific settings,
                such as template contest to inherit userlist, contest
                with problemson creating TESTS etc)

    section - title of section to edit

    section_no - there may be several sections with the same title: this parameter
                 is the order of such a section, starting from zero
                 choose string 'all' to edit all sections with such secion title
    option - option title to edit; you MUST specify this parameter
    value - string to set the ootion value, or
            True (default) to set empty value, or
            False to delete option from config (with or without value,
            works even if such option doesn't exist)

    Preserve comments at the top and at the bottom of the file.
    Make empty line between sections and delete them inside section.
    Add log comment at the bottom.

    '''
    if path is None:
        if contests is None:
            raise RuntimeError
        elif type(contests) == int:
            path = get_contest_path_conf(contests)
            edit_serve_cfg(path, None, function)
        elif type(contests) == str and contests == 'all':
            for contest in all_contests():
                path = get_contest_path_conf(contest)
                print(path)
                edit_serve_cfg(path, None, function)
        elif type(contests) == str and contests == 'regular':
            for contest in regular_contests():
                path = get_contest_path_conf(contest)
                edit_serve_cfg(path, None, function)
        else: #list of numbers
            for contest in contests:
                path = get_contest_path_conf(contest)
                edit_serve_cfg(path, None, function)
    else:
      if os.path.isfile(os.path.join(path, 'serve.cfg')):
        try:
           contest = EjudgeContestCfg(os.path.join(path, 'serve.cfg'))
        except:
            print(path)
            raise

        try:
            log_message = function(contest.config)
        except:
            print(path)
            raise
        rewrite_serve_cfg(path, contest.printconf(), log_message)
      else:
        print('no such file: ' + os.path.join(path, 'serve.cfg'))


class AddSectionCmd:
    def __init__(self, section, options):
        self.section = section
        self.options = options

    def __call__(self, config):
        idx = config.add_section(self.section)
        for option in self.options:
            if option[1] is True:
                config.set(self.section, idx, option[0], None)
            else:
                config.set(self.section, idx, option[0], option[1])
        return "added " + self.section + "[" + str(idx) +  "]:" + str(self.options)


class ApplySectionCmd:
    def __init__(self, section, filterF, actionF):
        self.section = section
        self.filterF = filterF
        self.actionF = actionF

    def __call__(self, config):
        for i in  range(100):
            try:
                items = config.options(self.section, i)
            except IndexError:
                break
            if filter(config, self.section, i):
                actionF(config, section, i)

class SetOptionCmd:
    def __init__(self, section, section_no, option, value):
        self.section = section
        self.section_no = section_no
        self.option = option
        self.value = value

    def __call__(self, config):
        if self.value is True:
            config.set(self.section, self.section_no, self.option, None)
        else:
            config.set(self.section, self.section_no, self.option, self.value)
        return self.section + "[" + self.section_no + "]:" + option + ' --> ' + str(valse)


class GroupCmd:
    def __init__(self, *args):
        self.args = args

    def __call__(self, config):
        log_message = ""
        for func in self.args:
            log_message += func(config)
        return log_message


class RemoveOptionCmd:
    def __init__(self, section, section_no, option):
        self.section = section
        self.section_no = section_no
        self.option = option


    def __call__(self, config):
        config.remove_option(self.section, self.section_no, self.option)
        return self.section + "[" + self.section_no + "]: remove " + option





def undo_serve_cfg(path = None, version = None):
    ''' UNDO specified in path serve.cfg or all serve.cfg in ejudge 
        (if path is None) to specified version)
    '''
    if version is None:
        raise RuntimeError
    if path is None:
        for contest in all_contests():
            path = HOME_JUDGES + '0'*(6-len(str(contest))) + str(contest) + '/conf/'
            undo_serve_cfg(path = path, version = version)
    else:
        path = os.path.join(path, 'serve.cfg')
        if os.path.isfile(path + str(version)):
            shutil.copy(path, path + version_stamp)
            shutil.copy(path + str(version), path)


def create_serve_cfg_table(section='default', section_no=0):
    columns = dict()
    header = '<tr><td>contest</td>'
    contests = dict()
    i = 1
    for contest_id in sorted(all_contests()):
            cfg_file = HOME_JUDGES + contest_id + '/conf/serve.cfg'
              #print cfg_file
            try:
                contest = EjudgeContestCfg(cfg_file)
            except IOError:
                pass
            except UnicodeDecodeError:
                print(cfg_file)
            except KeyError:
                print(cfg_file)
            options = contest.config.options(section, section_no)
            contests[contest_id] = [contest_id] + [""] * 100
            for opt in options:
                if opt not in columns.keys():
                    columns[opt] = i
                    header += "<td>" + opt + "</td>"
                    i += 1
                contests[contest_id][columns[opt]] = contest.config.get(section, section_no, opt) or 'True'
    header += "</tr>\n"
    print("<table border=1>\n" + header)
    print ("\n".join(["<tr><td>" + "</td><td>".join(contests[k]) + "</td></tr>"  for k in contests.keys()]) + "</table>").encode("utf-8")
    #for k in contests.keys():
    #    print contests[k]

def rewrite_serve_cfg(path, new_content, log_comment):
    '''Moves path/serve.cfg to path/serve.cfg[datetime stamp].
       Changes content of path/serve.cfg (except top and bottom comments by new_comment
       Adds log_comment to the bottom
    '''
    file = os.path.join(path, 'serve.cfg')
    if os.path.isfile(file):
        newfile = file + version_stamp
        shutil.copy(file, newfile)
        with open(file) as f:
            old_content = f.readlines()
        fnew = open(file, "w", encoding='utf-8')

        i = 0
        while old_content[i].startswith('#'):
            fnew.write(old_content[i])
            i += 1

        fnew.write('\n' + new_content + '\n')

        i = -1
        while not old_content[i].strip() or old_content[i].startswith('#'):
            i -= 1

        fnew.write("".join(old_content[i+1:]))

        fnew.write("# " + log_comment + " (backup written to serve.cfg" + version_stamp +")\n")
        fnew.close()
    else:
        raise IOError

def filter_by_lang_id(config, section, idx):
    value = config.get(section, idx, 'id')
    print(value)
    if str(value[0]) == '8':
        return True
    return False

def action_remove_item(config, section, idx):
    config.remove_option(section, idx, 'arch')

#create_serve_cfg_table('problem',2)
#print(list(regular_contests()))
#undo_serve_cfg(version = 543059717)
config = EjudgeContestCfg('serve.cfg')
#print(config.printconf())
#edit_serve_cfg(contests='regular', section='default', section_no = 0, value = False, option = 'enable_full_archive')
edit_serve_cfg(contests='regular', function=GroupCmd(AddSectionCmd('language',
[
    ['id', '31'],
    ['compile_id', '63'],
    ['long_name', '"1C 8.3"'],
    ['arch', '"1c"'],
    ['src_sfx', '".1c"'],
    ['short_name', '"1c"'],
]), AddSectionCmd('tester',
[
    ['name', 'Linux-1c'],
    ['abstract', True],
    ['no_core_dump', True],
    ['arch', '"1c"'],
    ['kill_signal', 'INT'],
    ['start_cmd', '"Run1C"'],
    ['check_dir', '"work-disk/work"'],
    ['start_env', '"EJUDGE_PREFIX_DIR"'],
]),AddSectionCmd('tester',
[
    ['any', True],
    ['super', 'Linux-1c'],
    ['arch', '1c'],
])))
