from data.oc import Oc
from data.db_session import create_session


def find_coincidences(oc_id):
    cncdns = {}
    db_sess = create_session()
    oc = db_sess.query(Oc).filter(Oc.id == oc_id).all()
    for row in oc.rows:
        for o in row.ocs:
            if o != oc:
                if o.img not in cncdns.keys():
                    cncdns[o.img] = 1
                else:
                    cncdns[o.img] += 1
    return cncdns

