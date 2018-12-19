class DBRouter(object):
    def db_for_read(self,model,**hints):
        return 'slave1'
    def db_for_write(self,model,**hints):
        return 'default'
    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True