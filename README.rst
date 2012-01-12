How to Install
============================

Mac OS X
----------------
::
    
    curl https://raw.github.com/gist/1224448/74d3fa70bb7a8ca3c7a87624c52b23c1b1248e52/kommonz.sh | bash

Ubuntu (Debian)
------------------------------
::
    
    wget -q -O - https://raw.github.com/gist/1224448/74d3fa70bb7a8ca3c7a87624c52b23c1b1248e52/kommonz.sh | bash

See `Wiki <https://github.com/kawazrepos/Kommonz/wiki/Kommonzのインストール>`_ for detail.

.. Note::

    **PilNotAvailable: Python Imaging Library is required for this formatter** エラーが出る場合多分PILのバージョンが低い
    ので以下コマンドで再インストールするべし::

        pip install PIL -U

    これでもダメなら下記の（様な）コマンドでリンクを貼れば良い（インストールされてるバージョンの違いなどで場所は変わる）::

        ln -s site-packages/PIL-1.1.7-py2.7-macosx-10.6-x86_64.egg site-packages/PIL

    あと "The _imagingft C module is not installed" とか表示される場合は ``libfreetype`` がない状態でPILをコンパイルしてしまっているので
    https://gist.github.com/1229763 か https://gist.github.com/1225180 で適切なOSのパッチを当ててからPILを以下コマンドで再インストールすれば良い::

        pip install PIL -U

