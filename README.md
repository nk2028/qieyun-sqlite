# _Guangyun_ [![Build status](https://ci.appveyor.com/api/projects/status/94tnbkamru7vk0iu?svg=true)](https://ci.appveyor.com/project/chromezh/guangyun)

_Guangyun_ (廣韻) SQLite database for Traditional Chinese Phonology

## Usage

The database could be accessed at `https://sgalal.github.io/Guangyun/data.sqlite3`.

**Tables**

`rhymes`: 韻

* `name`: 韻
* `rhyme_group`: 韻系（舉平以該上去入，以及祭泰夬廢）
* `tone`: 聲調（1-4）

`small_rhymes`: 小韻

* `id`
* `name`: 韻
* `of_rhyme`: 對應韻
* `initial`: 聲母（三十八聲母系統）
* `rounding`: 開合
* `division`: 等（1-4）
* `upper_char`: 反切上字
* `lower_char`: 反切下字

`character_entities`: 字頭

* `id`
* `name`: 字頭
* `of_small_rhyme`: 對應小韻
* `num_in_small_rhyme`: 在小韻中的序號
* `explanation`: 解釋

See [_Guangyun_](https://sgalal.github.io/Ghehlien/guangyun.html) for a detailed description.

## Featured Users

* [sgalal/Ghehlien](https://github.com/sgalal/Ghehlien)
* [sgalal/brogue](https://github.com/sgalal/brogue)

## Acknowledgements

* [YonhTenxMyangx](https://github.com/BYVoid/ytenx) - Source of _Guangyun_ data

## License

Code for constructing database is distributed under MIT license.

_Guangyun_ data is from YonhTenxMyangx, distributed with its original license.
