# 先升级python2.6到2.7
http://www.cnblogs.com/ouxingning/archive/2012/10/24/install_python_on_centos.html

$ yum install zlib-devel
$ yum install bzip2-devel
$ yum install openssl-devel
$ yum install ncurses-devel

$ cd /usr/local/src/
$ wget http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.bz2
$ tar xf Python-2.7.8.tar.bz2
$ cd Python-2.7.8
$ ./configure --prefix=/usr/local
$ make && make altinstall

安装上面步骤安装好之后，软链到替换原先的python
$ mv /usr/bin/python /usr/bin/python2.6.6
$ ln -s /usr/local/bin/python2.7 /usr/bin/python

最后把yum的默认python执行文件改回去
$ vim /usr/bin/yum
$ /usr/bin/python2.6.6

重新安装setuptools，不能用yum安装了，yum安装的还是2.7的，因为yum只支持2.6
参考: https://pypi.python.org/pypi/setuptools

具体步骤:
$ cd /usr/local/src/
$ wget https://bootstrap.pypa.io/ez_setup.py -O - | python

# 创建用户和用户组
$ su - root
$ groupadd users
$ useradd user_00 -g users

$ mkdir -p /data/code
$ mkdir -p /data/release
$ chown user_00:users -R /data

# 安装nginx
参考:
http://www.cnblogs.com/kunhu/p/3633002.html
http://nginx.org/download/

具体步骤:
$ yum install -y pcre-devel
$ yum install -y zlib-devel

$ cd /usr/local/src/
$ wget http://nginx.org/download/nginx-1.8.0.tar.gz
$ tar -zxvf nginx-1.8.0.tar.gz
$ ./configure --prefix=/usr/local/nginx
$ make && make install

$ /usr/local/nginx/sbin/nginx -t

放到service启动
参考:
https://www.nginx.com/resources/wiki/start/topics/examples/redhatnginxinit/

$ vim /etc/init.d/nginx
$ chmod 755 /etc/init.d/nginx
$ chkconfig --add nginx

# 配置gunicorn
pip install gunicorn

# 配置supervicor
pip install supervisor

# 生成sshkey
$ sshkey-gen
$ cat ~/.ssh/id_rsa.pub
拷贝到github

$ cd /data/code
$ git clone git@github.com:kevin386/microblog.git

# 编辑环境变量:
export PS1="\[\e[36;1m\]\u\[\e[0m\]@pythonil#\[\e[33;1m\]\h\[\e[0m\]:\[\e[31;1m\]\w\[\e[0m\]\n\$ "
export MODE='CN'
export MAIL_USERNAME='xx'
export MAIL_PASSWORD='xxx'

