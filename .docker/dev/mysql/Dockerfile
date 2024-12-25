FROM percona:8.0.34-26

RUN chown -R mysql:mysql /var/lib/mysql

ADD my.cnf /etc/mysql/conf.d/my.cnf

CMD ["mysqld"]

EXPOSE 3306