# 配置系统环境变量:
export PS1="\[\e[36;1m\]\u\[\e[0m\]@pythonil#\[\e[33;1m\]\h\[\e[0m\]:\[\e[31;1m\]\w\[\e[0m\]\n\$ "
export MODE='CN'
export MAIL_USERNAME='user@example.com'
export MAIL_PASSWORD='password'

# 升级系统python2.6到2.7
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

# 生成sshkey
$ ssh-keygen
$ cat ~/.ssh/id_rsa.pub
复制sshkey并配置到到github

# 拉取代码
$ mkdir -p /data/code
$ mkdir -p /data/release
$ chown user_00:users -R /data
$ cd /data/code
$ git clone git@github.com:kevin386/microblog.git
$ ln -s /data/code/microblog /data/release/microblog

# 安装nginx
参考:
http://www.cnblogs.com/kunhu/p/3633002.html
http://nginx.org/download/

yum install -y pcre-devel
yum install -y zlib-devel
yum install -y openssl openssl-devel

$ cd /usr/local/src/
$ wget http://nginx.org/download/nginx-1.8.0.tar.gz
$ tar -zxvf nginx-1.8.0.tar.gz
$ cd nginx-1.8.0

./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-mail --with-mail_ssl_module --with-file-aio --with-ipv6 --with-http_spdy_module --with-cc-opt='-O2 -g -pipe -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic'
make && make install

链接配置文件
$ mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
$ ln -s /data/release/microblog/deploy/nginx.conf /etc/nginx/nginx.conf

创建配置中的用户和目录
useradd --system --home-dir=/var/cache/nginx --shell=/sbin/nologin nginx
mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp /var/cache/nginx/fastcgi_temp /var/cache/nginx/uwsgi_temp /var/cache/nginx/scgi_temp

测试配置
/usr/sbin/nginx -t

加到service服务
参考:
https://www.nginx.com/resources/wiki/start/topics/examples/redhatnginxinit/

$ vim /etc/init.d/nginx
$ chmod 755 /etc/init.d/nginx
$ chkconfig --add nginx
$ chkconfig --list | grep nginx

启动nginx
service nginx start/stop/status/restart

# 安装mysql-server
$ yum install mysql-devel
$ yum install mysql-server
$ mysql_install_db

设置root密码
$ /usr/bin/mysqladmin -u root password 'xxxxx'

软链配置:
$ mv /etc/my.cnf /etc/my.cnf.bak
$ ln -s /data/release/microblog/deploy/my.conf /etc/my.cnf

启动server
$ chkconfig --add mysqld
$ service mysqld start

新建读写用户和数据库
mysql> create database blog;
mysql> CREATE USER 'rwuser'@'localhost' IDENTIFIED BY 'xxxx';
mysql> grant all privileges on blog.* to rwuser@localhost identified by 'xxxx';
mysql> flush privileges;

# 安装python-mysql
$ easy_install MySQL-python

# 配置supervicor
pip install supervisor
$ ln -s /data/release/microblog/deploy/supervisord.conf /etc/supervisord.conf
$ ln -s /data/release/microblog/deploy/sv.ini /etc/sv.ini

# 配置gunicorn等python三方软件
cd /data/release/microblog/deploy
pip wheel -r requirements.txt

# 测试gunicorn启动
cd /data/release/microblog
mkdir tmp
touch tmp/main.log

