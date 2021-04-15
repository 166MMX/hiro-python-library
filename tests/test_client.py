import datetime
import json
import tempfile
from collections import namedtuple
from typing import List
from uuid import uuid4

import pytest
import requests
from requests import HTTPError, Response

from arago.hiro.client.client import HiroClient
from arago.hiro.client.exception import HiroClientError, OntologyValidatorError
from arago.hiro.model.graph.vertex import Vertex
from arago.hiro.model.storage import BlobId, TimeSeriesValue, TimeSeriesId
from arago.ogit import OgitEntity


def uuid() -> str:
    return str(uuid4())


class TestClassEdgeCreate:
    def test_sig_args_str_str_str(self, client: HiroClient):
        # ogit:Account ogit:connects  ogit:Person - fails due to graphit error ogit:email missing
        # ogit:Attachment ogit:belongs  ogit:Comment
        # when:
        vertex_a = client.model.graph.vertex.create('ogit/Attachment')
        vertex_b = client.model.graph.vertex.create('ogit/Comment')
        edge_c = client.model.graph.edge.create(vertex_a.id, 'ogit/belongs', vertex_b.id)

        # then:
        assert edge_c.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(vertex_a)
        assert deleted.is_deleted is True
        deleted = client.model.graph.vertex.delete(vertex_b)
        assert deleted.is_deleted is True


class TestClassEdgeDelete:
    def test_sig_args_edge_id(self, client: HiroClient):
        # ogit:Account ogit:connects  ogit:Person - fails due to graphit error ogit:email missing
        # ogit:Attachment ogit:belongs  ogit:Comment
        # when:
        vertex_a = client.model.graph.vertex.create('ogit/Attachment')
        vertex_b = client.model.graph.vertex.create('ogit/Comment')
        edge_c = client.model.graph.edge.create(vertex_a.id, 'ogit/belongs', vertex_b.id)
        assert edge_c.created_by is not None

        # then:
        edge_d = client.model.graph.edge.delete(edge_c.id)
        assert edge_d.is_deleted is True

        # cleanup:
        deleted = client.model.graph.vertex.delete(vertex_a)
        assert deleted.is_deleted is True
        deleted = client.model.graph.vertex.delete(vertex_b)
        assert deleted.is_deleted is True


class TestClassGraphVertexCreate:
    def test_sig_args_type(self, client: HiroClient):
        # when:
        created = client.model.graph.vertex.create('ogit/Note')

        # then:
        assert created.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True

    def test_sig_args_dict(self, client: HiroClient, user_agent: str):
        # when:
        created = client.model.graph.vertex.create({
            'ogit/_type': 'ogit/Note'
        })

        # then:
        assert created.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True

    def test_sig_args_vertex(self, client: HiroClient, user_agent: str):
        # when:
        created = client.model.graph.vertex.create(Vertex({
            'ogit/_type': 'ogit/Note'
        }))

        # then:
        assert created.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True

    def test_sig_args_type_dict(self, client: HiroClient, user_agent: str):
        # when:
        created = client.model.graph.vertex.create('ogit/Note', {
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })

        # then:
        assert created.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True

    def test_vertex_create_args_type_vertex(self, client: HiroClient, user_agent: str):
        # when:
        created = client.model.graph.vertex.create('ogit/Note', Vertex({
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))

        # then:
        assert created.created_by is not None

        # cleanup:
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True


class TestClassGraphVertexGet:
    def test_vertex_get(self, client: HiroClient):
        vertex = client.model.graph.vertex.get('ogit/Node')
        assert vertex.id == 'ogit/Node'
        assert vertex.created_by is not None

    def test_vertex_get_fields(self, client: HiroClient):
        vertex = client.model.graph.vertex.get('ogit/Node', {'ogit/_id'})
        assert vertex.created_by is None

    @pytest.mark.skip
    def test_vertex_get_by_xid(self, client: HiroClient):
        g = client.model.graph.vertex.get_by_xid('arago.co')
        vertex = next(g)
        with pytest.raises(StopIteration):
            next(g)
        assert vertex.type == 'ogit/Organization'
        assert vertex.created_by is not None

    @pytest.mark.skip
    def test_vertex_get_by_xid_fields(self, client: HiroClient):
        g = client.model.graph.vertex.get_by_xid('arago.co', {'ogit/_id'})
        vertex = next(g)
        with pytest.raises(StopIteration):
            next(g)
        assert vertex.created_by is None


class TestClassGraphVertexUpdate:
    # noinspection PyTypeChecker,PyArgumentList
    def test_vertex_update_usage(self, client: HiroClient):
        created = client.model.graph.vertex.create('ogit/Note')
        with pytest.raises(TypeError):
            client.model.graph.vertex.update(created.id, '')
        with pytest.raises(TypeError):
            client.model.graph.vertex.update(3, {
                'ogit/name': uuid(),
            })
        with pytest.raises(TypeError):
            client.model.graph.vertex.update(vertex_id=created.id, vertex='')
        with pytest.raises(TypeError):
            client.model.graph.vertex.update(vertex_id=3, vertex={
                'ogit/name': uuid(),
            })
        with pytest.raises(TypeError):
            client.model.graph.vertex.update(vertex=3)
        with pytest.raises(KeyError):
            client.model.graph.vertex.update(vertex_type='')
        # with pytest.raises(RuntimeError):
        #     client.model.graph.vertex.update(vertex_id=created.id)
        with pytest.raises(RuntimeError):
            client.model.graph.vertex.update(created.id, {
                'ogit/name': uuid(),
            }, 2)
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.v == 2
        assert deleted.is_deleted is True

    def test_vertex_update_1(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(created.id, {
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_2(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update({
            'ogit/_id': created.id,
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_3(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(created.id, Vertex({
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))
        assert updated.v == 2
        deleted = updated.delete()
        assert deleted.is_deleted is True

    def test_vertex_update_4(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(Vertex({
            'ogit/_id': created.id,
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_5(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(created.id, vertex={
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_6(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(vertex_id=created.id, vertex={
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_7(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(created.id, vertex=Vertex({
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_8(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(vertex_id=created.id, vertex=Vertex({
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_9(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(vertex={
            'ogit/_id': created.id,
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        })
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True

    def test_vertex_update_10(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        updated = client.model.graph.vertex.update(vertex=Vertex({
            'ogit/_id': created.id,
            'ogit/name': uuid(),
            'ogit/content': 'Unit Test: %s' % user_agent,
        }))
        assert updated.v == 2
        deleted = client.model.graph.vertex.delete(updated.id)
        assert deleted.is_deleted is True


class TestClassGraphVertexDelete:
    def test_vertex_delete_1(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(created)
        assert deleted.is_deleted is True

    def test_vertex_delete_2(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(created.to_dict())
        assert deleted.is_deleted is True

    def test_vertex_delete_3(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(created.id)
        assert deleted.is_deleted is True

    def test_vertex_delete_4(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(vertex=created)
        assert deleted.is_deleted is True

    def test_vertex_delete_5(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(vertex={
            'ogit/_id': created.id
        })
        assert deleted.is_deleted is True

    def test_vertex_delete_6(self, client: HiroClient, user_agent: str):
        created = client.model.graph.vertex.create('ogit/Note')
        deleted = client.model.graph.vertex.delete(vertex_id=created.id)
        assert deleted.is_deleted is True


class TestClassOntologyValidator:
    def test_create_missing_mandatory(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Alert.ttl
        with pytest.raises(OntologyValidatorError):
            client.model.graph.vertex.create('ogit/Alert')
        res = client.model.graph.vertex.create('ogit/Alert', {
            'ogit/type': 'foo',
            'ogit/category': 'foo',
            'ogit/creator': 'foo',
        })
        assert res.id is not None
        res = res.delete()
        assert res.is_deleted is True

    def test_update_not_declared(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Note.ttl
        note = client.model.graph.vertex.create('ogit/Note')
        with pytest.raises(OntologyValidatorError):
            res = note.update({
                'ogit/description': 'foo'
            })
        note = note.delete()
        assert note.is_deleted is True

    def test_create_broken_person_email_missing(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Person.ttl
        with pytest.raises(HiroClientError) as info:
            client.model.graph.vertex.create('ogit/Person')
        assert info.value.args[0] == 'ogit/email is missing'

    def test_create_broken_person_email_foo(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Person.ttl
        with pytest.raises(HiroClientError) as info:
            client.model.graph.vertex.create('ogit/Person', {
                'ogit/email': 'foo',
            })
        assert info.value.args[0] == 'foo already exists'

    def test_create_broken_person_email_uuid(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Person.ttl
        res = client.model.graph.vertex.create('ogit/Person', {
            'ogit/email': uuid(),
        })
        print(json.dumps(res.to_dict(), indent=2))
        res.delete()

    def test_create_broken_organization_name_missing(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Organization.ttl
        with pytest.raises(HiroClientError) as info:
            client.model.graph.vertex.create('ogit/Organization')
        assert info.value.args[0] == 'ogit/name is missing'

    def test_create_broken_organization_name_foo(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Organization.ttl
        with pytest.raises(HiroClientError) as info:
            client.model.graph.vertex.create('ogit/Organization', {
                'ogit/name': 'foo',
            })
        assert info.value.args[0] == 'foo already exists'

    def test_create_broken_organization_name_uuid(self, client: HiroClient):
        # https://github.com/arago/OGIT/blob/master/SGO/sgo/entities/Organization.ttl
        res = client.model.graph.vertex.create('ogit/Organization', {
            'ogit/name': uuid(),
        })
        print(json.dumps(res.to_dict(), indent=2))
        res.delete()


class TestClassGraphSearch:
    def test_elastic_search(self, client: HiroClient):
        res = client.model.search.index(r'+ogit\/_xid')
        res_list = list(res)
        assert len(res_list) > 4


class TestClassStorage:
    def test_blob_model_set(self, client: HiroClient):
        # when:
        blob = client.model.graph.vertex.create('ogit/Attachment')

        # then:
        with tempfile.TemporaryFile() as fp:
            with requests.request('get', 'https://docs.hiro.arago.co/_images/HIRO.png') as r:
                fp.write(r.content)
            fp.seek(0)
            client.model.storage.blob.set(BlobId(blob.id), fp)

        # cleanup:
        # blob.delete()

    # noinspection SpellCheckingInspection
    def test_blob_model_get(self, client: HiroClient):
        blob_id = BlobId('ckgmbomiu91cu5a02jyxuodv2')
        with open('/Users/jharth/test.png', 'wb') as fp:
            with client.model.storage.blob.get(blob_id) as g:
                for b in g:
                    fp.write(b)

        # when:
        # then:
        # cleanup:

    def test_ts_model_add(self, client: HiroClient):
        ts = client.model.graph.vertex.create(OgitEntity.OGIT_TIME_SERIES.value.name.uri)

        def g():
            with open('/Users/jharth/Downloads/AviationData.csv', encoding='latin_1') as f:
                import csv
                r = csv.reader(f, delimiter=',', quotechar='"')
                header = next(r)
                Record = namedtuple('Record', map(lambda it: str(it).replace('.', '_'), header))
                row: List[str]
                for row in r:
                    rec = Record(*row)
                    timestamp = datetime.datetime.combine(
                        datetime.date.fromisoformat(rec.Event_Date),
                        datetime.time(),
                        datetime.timezone.utc)
                    yield TimeSeriesValue(rec.Event_Id, timestamp)

        client.model.storage.ts.add(TimeSeriesId(ts.id), g())
        pass

    def test_ts_model_get(self, client: HiroClient):
        pass


class TestClassIdentityAccountManagement:
    @pytest.mark.skip
    def test_iam_self(self, client: HiroClient):
        r = client.model.iam.self.compatibility()
        r = client.model.iam.self.roles()
        r = client.model.iam.self.account()
        # r = client.iam.self.person()
        pass

    @pytest.mark.skip
    def test_iam_roles(self, client: HiroClient):
        r = client.model.iam.roles.list()

    @pytest.mark.skip
    def test_iam_accounts(self, client: HiroClient):
        r = client.model.iam.accounts.list()


class TestClassApplication:
    @pytest.mark.skip
    def test_app_graph(self, client: HiroClient):
        name = str(uuid())
        description = 'Unit Test: %s' % client.session.headers['User-Agent']
        application = client.model.app.graph.create(name, description)
        credentials = client.model.app.graph.activate(application.id)
        r1 = client.model.app.graph.deactivate(application.id)
        pass

    @pytest.mark.skip
    def test_desktop_graph(self, client: HiroClient):
        name = str(uuid())
        description = 'Unit Test: %s' % client.session.headers['User-Agent']
        result = client.model.search.index(' '.join([
            r'+ogit\/_type:"ogit/Auth/Application"',
            r'+ogit\/Auth\/Application\/type:"ui"',
            r'+ogit\/Auth\/Application\/status:"active"',
            r'+ogit\/Auth\/Application\/urls:"graph://apps/hiro-desktop/"',
        ]))
        desktop_application = next(result)
        application = client.model.app.desktop.create(name, description, desktop_application.id, 'public')
        r1 = client.model.app.desktop.activate(application.id)
        r2 = client.model.app.desktop.deactivate(application.id)
        pass

    @pytest.mark.skip
    def test_app_manifest(self, client: HiroClient):
        r1 = client.model.search.index(r'+ogit\/_type:"ogit/Auth/Application"')
        l1 = list(r1)
        ui_apps = [v for v in l1 if v['ogit/Auth/Application/type'] == 'ui']
        desktop_apps = [v for v in l1 if v['ogit/Auth/Application/type'] == 'desktop']
        graph_apps = [v for v in l1 if v['ogit/Auth/Application/type'] == 'graph']
        l2 = list(v.id for v in l1)
        having_manifest = []
        r3 = []
        for i in l2:
            try:
                r2 = client.model.app.desktop.manifest(i)
                print(r2)
                r3.append(r2)
                having_manifest.append(i)
            except HiroClientError as e:
                error: HTTPError = e.args[1]
                response: Response = error.response
                if response.status_code != 404:
                    raise e
            pass
        l3 = [v for v in l1 if v.id in having_manifest]
        pass

    @pytest.mark.skip
    def test_ui_graph(self, client: HiroClient):
        name = str(uuid())
        description = 'Unit Test: %s' % client.session.headers['User-Agent']
        application = client.model.app.web.create(name, description)
        r1 = client.model.app.web.activate(application.id, ['https://unit.test.example'])
        r2 = client.model.app.web.deactivate(application.id)
        pass


class TestClass:
    def test_vertex_crud(self, client: HiroClient, user_agent: str):
        note = client.model.graph.vertex.create('ogit/Note')
        assert note.type == OgitEntity.OGIT_NOTE
        note2 = client.model.graph.vertex.get(note.id)
        assert note2.id == note.id
        s = uuid()
        note2['ogit/name'] = s
        note2['ogit/content'] = 'Unit Test: %s' % user_agent
        note2.xid = s
        updated = client.model.graph.vertex.update(note2)
        assert updated['ogit/content'] == 'Unit Test: %s' % user_agent
        # g = client.model.graph.vertex.get_by_xid(note2.xid)
        # note3 = next(g)
        # with pytest.raises(StopIteration):
        #     next(g)
        # assert note3['ogit/name'] == s
        deleted = client.model.graph.vertex.delete(note.id)
        assert deleted.is_deleted is True

    # TODO         g = client.model.graph.search.elastic_search(r'+ogit\/_xid') contains _xid: None
    # TODO         g = client.model.graph.search.elastic_search(r'+ogit\/_xid:*') contains _xid: with data

    def test_vertex_validation(self, client: HiroClient, user_agent: str):
        note = client.model.graph.vertex.create('ogit/Note')
        assert note.type == OgitEntity.OGIT_NOTE
        note['ogit/name'] = uuid()
        note['ogit/description'] = 'Unit Test: %s' % user_agent
        with pytest.raises(OntologyValidatorError):
            client.model.graph.vertex.update(note)
        deleted = client.model.graph.vertex.delete(note.id)
        assert deleted.is_deleted is True

    def test_gremlin_api(self, client: HiroClient):
        gen = client.model.search.graph('ogit/Node', 'out()')
        lst = list(gen)
        assert len(lst) == 14

    @pytest.mark.skip
    def test_health_ok(self, client: HiroClient):
        health = client.model.health.check()
        assert health['status'] == 'ok'
        assert health['description'] == 'The service is healthy :)'

    @pytest.mark.skip
    def test_identity(self, client):
        r = client.model.identity.get()
        assert r['ogit/_type'] == 'ogit/Auth/Account'
