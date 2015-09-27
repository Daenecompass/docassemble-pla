import psycopg2
from docassemble.webapp.config import daconfig
from base64 import b64decode
from docassemble.base.core import DAObject

class LegalServer(DAObject):
    def init(self):
        self.connected = False
        return super(LegalServer, self).init()
    def __del__(self):
        if self.connected:
            self.conn.close()
        return
    def connect(self):
        legalserver = daconfig.get('legalserver', None)
        if legalserver is None:
            raise Exception("Could not get Legal Server connection information")
        try:
            self.conn = psycopg2.connect("dbname='" + legalserver['database'] + "' user='" + legalserver['username'] + "' host='" + legalserver['host'] + "' password='" + legalserver['password'] + "'")
        except Exception as e:
            raise Exception("Could not connect to Legal Server: " + str(e))
        self.connected = True
        return
    def lookup_unique_id(self, unique_id):
        cur = self.conn.cursor()
        cur.execute("""select m.identification_number, up.first as sfname, up.last as slname, up.email as semail, c.first as cfname, c.last as clname, c.email as cemail, map.office_name, lookup_citizenship_statuses.name as cstatus, up.phone_business as sphone from matter as m left outer join matter_assignment_primary as map on (m.id=map.matter_id) left outer join users as u on (map.user_id=u.id) left outer join person as up on (u.person_id=up.id) left outer join person as c on (m.person_id=c.id) left outer join lookup_citizenship_statuses on (m.citizenship_status=lookup_citizenship_statuses.id) where m.unique_id=%s""", (str(unique_id),))
        rows = cur.fetchall()
        result = dict()
        for row in rows:
            result['identification_number'] = row[0]
            result['sfname']                = row[1]
            result['slname']                = row[2]
            result['semail']                = row[3]
            result['cfname']                = row[4]
            result['clname']                = row[5]
            result['cemail']                = row[6]
            result['office_name']           = row[7]
            result['cstatus']               = row[8]
            result['sphone']                = row[9]
        if 'identification_number' not in result:
            raise Exception("Could not retrieve information about unique_id")
        return(result)
            
class LegalServerCase(DAObject):
    def init(self):
        self.retrieved = False
        return super(LegalServerCase, self).init()
    def retrieve(self, encoded_unique_id):
        unique_id = b64decode(encoded_unique_id)
        legalserver = LegalServer()
        legalserver.connect()
        self.fields = legalserver.lookup_unique_id(unique_id)
        self.retrieved = True
        return

    
    
  
