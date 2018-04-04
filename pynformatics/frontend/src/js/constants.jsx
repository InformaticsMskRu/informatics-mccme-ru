export const LANGUAGES = {
  1: {
    name: 'Free Pascal 2.6.2',
    extension: '.pas',
    mime: 'text/x-pascal',
  },
  2: {
    name: 'GNU C 4.9',
    extension: '.c',
    mime: 'text/x-csrc',
  },
  3: {
    name: 'GNU C++ 4.9',
    extension: '.cpp',
    mime: 'text/x-c++src',
  },
  7: {
    name: 'Turbo Pascal',
    extension: '.pas',
    mime: 'text/x-pascal',
  },
  8: {
    name: 'Borland Delphi 6 - 14.5',
    extension: '.pas',
    mime: 'text/x-pascal',
  },
  9: {
    name: 'Borland C',
    extension: '.c',
    mime: 'text/x-csrc',
  },
  10: {
    name: 'Borland C++',
    extension: '.cpp',
    mime: 'text/x-c++src',
  },
  18: {
    name: 'Java JDK 1.7',
    extension: '.java',
    mime: 'text/x-java',
  },
  22: {
    name: 'PHP 5.2.17',
    extension: '.php',
    mime: 'text/x-php',
  },
  23: {
    name: 'Python 2.7',
    extension: '.py',
    mime: 'text/x-python',
  },
  24: {
    name: 'Perl 5.10.1',
    extension: '.pl',
    mime: 'text/x-perl',
  },
  25: {
    name: 'Mono C# 2.10.8.0',
    extension: '.cs',
    mime: 'text/x-csharp',
  },
  26: {
    name: 'Ruby 1.8.7',
    extension: '.rb',
    mime: 'text/x-ruby',
  },
  27: {
    name: 'Python 3.3',
    extension: '.py',
    mime: 'text/x-python',
  },
  28: {
    name: 'Haskell GHC 7.4.2',
    extension: '.hs',
    mime: 'text/x-haskell',
  },
  29: {
    name: 'FreeBASIC 1.00.0',
    extension: '.bas',
  },
  30: {
    name: 'PascalABC 1.8.0.496',
    extension: '.pas',
    mime: 'text/x-pascal',
  },
  // 31: {
  //   name: '1C 8.3',
  //   extension: '.1c',
  // },
};


export const STATUSES = {
  NaN: {
    short: 'ER',
    long: 'Server error',
    color: 'blue',
  },
  0: {
    short: 'OK',
    long: 'ОК',
    color: 'green',
  },
  1: {
    short: 'CE',
    long: 'Ошибка компиляции',
    color: 'orange',
  },
  2: {
    short: 'RT',
    long: 'Ошибка при работе программы',
    color: 'orange',
  },
  3: {
    short: 'TL',
    long: 'Ошибка превышения лимита времени',
    color: 'orange',
  },
  4: {
    short: 'PE',
    long: 'Ошибка неправильного формата результата',
    color: 'orange',
  },
  5: {
    short: 'WA',
    long: 'Неправильный ответ',
    color: 'orange',
  },
  6: {
    short: 'CF',
    long: 'Внутренняя ошибка проверки',
    color: 'blue',
  },
  7: {
    short: 'PT',
    long: 'Частичное решение',
    color: 'orange',
  },
  8: {
    short: 'AC',
    long: 'Принято на проверку',
    color: 'green',
  },
  9: {
    short: 'IG',
    long: 'Решение проигнорировано',
    color: 'orange',
  },
  10: {
    short: 'DQ',
    long: 'Решение дисквалифицировано',
    color: 'orange',
  },
  11: {
    short: 'PD',
    long: 'Ожидает проверки',
    color: 'green',
  },
  12: {
    short: 'ML',
    long: 'Ошибка превышения лимита памяти',
    color: 'orange',
  },
  13: {
    short: 'SE',
    long: 'Ошибка нарушения ограничений безопасности',
    color: 'orange',
  },
  14: {
    short: 'SV',
    long: 'Ошибка нарушения стиля оформления исходного кода',
    color: 'orange',
  },
  15: {
    short: 'WL',
    long: 'Ошибка превышения лимита реального времени',
    color: 'orange',
  },
  16: {
    short: 'PR',
    long: 'Ожидает подтверждения',
    color: 'green',
  },
  17: {
    short: 'RJ',
    long: 'Отклонено',
    color: 'orange',
  },
  18: {
    short: 'SK',
    long: 'Пропущено',
    color: 'orange',
  },
  95: {
    short: 'FR',
    long: 'Ожидает полной перепроверки',
    color: 'orange',
  },
  96: {
    short: 'RU',
    long: 'В очереди проверки или проверяется',
    color: 'orange'
  },
  97: {
    short: 'CD',
    long: 'Решение скомпилировно, но еще не отправлено на проверку',
    color: 'orange',
  },
  98: {
    short: 'CO',
    long: 'Compiling...',
    color: 'orange',
  },
  99: {
    short: 'RJ',
    long: 'Решение отправлено на перепроверку',
    color: 'orange',
  },
};
