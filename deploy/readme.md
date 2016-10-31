# 升级python到2.7.8
wget www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz
cd Python-2.7.8
./configure --enable-shared --prefix=/usr/local/python27

# 创建用户和用户组
su - root
groupadd users
useradd user_00 -g users

mkdir /data/code
mkdir /data/release
chown user_00:users -R /data

# 安装nginx
http://www.cnblogs.com/kunhu/p/3633002.html
http://nginx.org/download/
cd /usr/local/src/
wget http://nginx.org/download/nginx-1.9.8.tar.gz
tar -zxvf nginx-1.9.8.tar.gz
./configure --prefix=/usr/local/nginx
make && make install

yum -y install pcre-devel
yum install -y zlib-devel

/usr/local/nginx/sbin/nginx -t

放到service启动
https://www.nginx.com/resources/wiki/start/topics/examples/redhatnginxinit/
vim /etc/init.d/nginx
chmod 755 /etc/init.d/nginx
chkconfig --add nginx

# 安装git和pip
yum install git
yum install python-setuptools
easy_install pip
pip install gunicorn


su - user_00

pip install 

# 生成
sshkey-gen
cat ~/.ssh/id_rsa.pub
拷贝到github

cd /data/code
git clone git@github.com:kevin386/microblog.git

# 编辑环境变量:
export PS1="\[\e[36;1m\]\u\[\e[0m\]@pythonil#\[\e[33;1m\]\h\[\e[0m\]:\[\e[31;1m\]\w\[\e[0m\]\n\$ "
export MODE='CN'
export MAIL_USERNAME='xx'
export MAIL_PASSWORD='xxx'

