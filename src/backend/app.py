from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from typing import Set
from functools import lru_cache
import os
import re
import json


MAX_PLATFORMS: int = 5
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, "static")
DATA_ROOT = os.path.join(APP_ROOT, "../../../../data/")


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATA_ROOT}/data.db"
db = SQLAlchemy(app)


class Platform(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    nbr = db.Column(db.Integer, nullable=False)
    txt = db.Column(db.String, nullable=False)
    is_valid = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Platform {self.nbr} = {self.txt}>"

    def validate(self, validation_regex: str) -> None:
        regex = re.compile(validation_regex)
        match = regex.match(self.txt)
        if match:
            self.is_valid = True
        else:
            self.is_valid = False

    def to_json(self) -> str:
        schema = PlatformSchema(many=False)
        dumped = schema.dump(self)
        return jsonify(dumped)


class PlatformSchema(Schema):
    id = fields.Number()
    domain_id = fields.Number()
    nbr = fields.Number()
    txt = fields.Str()
    is_valid = fields.Boolean()


class Domain(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)

    platforms = db.relationship(
        "Platform",
        cascade="all,delete",
        backref=db.backref("domain", lazy=False),
    )

    def __repr__(self) -> str:
        return f"<Domain {self.id}: {self.name}>"

    def to_json(self) -> str:
        schema = DomainSchema(many=False)
        dumped = schema.dump(self)
        return jsonify(dumped)


class DomainSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    platforms = fields.Nested(PlatformSchema, many=True)


@lru_cache(maxsize=None)
def get_schema_from_file() -> str:
    try:
        with open(os.path.join(APP_STATIC, "schema.json"), "r") as schema_file:
            return schema_file.read()
    except:
        return '{"description":"", "regex":""}'


@lru_cache(maxsize=None)
def get_schema_regex() -> str:
    schema_json: str = get_schema_from_file()
    schema = json.loads(schema_json)
    if "regex" in schema:
        return schema["regex"]
    else:
        return ""


@app.route("/domains/<int:id>", methods=["GET"])
def get_domain(id: int) -> str:
    status_code: int = 200
    content: str = ""

    domain: Domain = Domain.query.get(id)
    if domain is None:
        status_code = 204
    else:
        regex = get_schema_regex()
        for platform in domain.platforms:
            platform.validate(regex)
        content = domain.to_json()

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/domains", methods=["GET"])
def get_domains() -> str:
    domain_objects = Domain.query.all()

    regex = get_schema_regex()
    for domain in domain_objects:
        for platform in domain.platforms:
            platform.validate(regex)

    schema = DomainSchema(many=True)
    domains = schema.dump(domain_objects)

    response = make_response(jsonify(domains), 200)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/domains", methods=["POST"])
def add_domain() -> str:
    data = request.json
    name = data["name"]

    new_domain: Domain = Domain(name=name)
    db.session.add(new_domain)
    db.session.commit()

    response = make_response(new_domain.to_json(), 201)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/domains", methods=["PUT"])
def update_domain() -> str:
    status_code: int = 202
    content: str = ""

    data = request.json
    id: int = data["id"]
    domain: Domain = Domain.query.get(id)
    if domain is None:
        status_code = 500
        content = f'{{"success":false,"message":"Could not find domain with ID {id}"}}'
    else:
        domain.name = data["name"]
        db.session.commit()
        content = domain.to_json()

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/domains/<int:id>", methods=["DELETE"])
def delete_domain(id: int) -> str:
    status_code: int = 202
    content: str = ""

    domain: Domain = Domain.query.get(id)
    if domain is None:
        status_code = 500
        content = f'{{"success":false,"message":"Could not find domain with ID {id}"}}'
    else:
        db.session.delete(domain)
        db.session.commit()
        content = f'{{"success":true,"message":"Deleted domain with ID {id}"}}'

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/domains/available_platforms/<int:id>", methods=["GET"])
def get_available_platforms(id: int) -> str:
    status_code: int = 200
    content: str = '{"available":[]}'

    platforms = Platform.query.filter_by(domain_id=id).all()
    if len(platforms) < MAX_PLATFORMS:
        available: Set[int] = {1, 2, 3, 4, 5}
        used: Set[int] = set()
        for platform in platforms:
            used.add(platform.nbr)
        available = available.difference(used)

        content = f'{{"available":[{",".join(str(s) for s in available)}]}}'

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/platforms/<int:id>", methods=["GET"])
def get_platform(id: int) -> str:
    status_code: int = 200
    content: str = ""

    platform: Platform = Platform.query.get(id)
    if platform is None:
        status_code = 204
    else:
        content = platform.to_json()

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/platforms", methods=["POST"])
def add_platform() -> str:
    data = request.json
    domain_id: int = data["domain_id"]
    nbr: int = data["nbr"]
    txt: str = data["txt"]
    is_valid: bool = data["is_valid"]

    new_platform: Platform = Platform(
        domain_id=domain_id, nbr=nbr, txt=txt, is_valid=is_valid
    )
    db.session.add(new_platform)
    db.session.commit()

    response = make_response(new_platform.to_json(), 201)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/platforms", methods=["PUT"])
def update_platform() -> str:
    status_code: int = 202
    content: str = ""

    data = request.json
    id: int = data["id"]
    platform: Platform = Platform.query.get(id)
    if platform is None:
        status_code = 500
        content = (
            f'{{"success":false,"message":"Could not find platform with ID {id}"}}'
        )
    else:
        platform.domain_id = data["domain_id"]
        platform.nbr = data["nbr"]
        platform.txt = data["txt"]
        platform.is_valid = data["is_valid"]
        db.session.commit()
        content = platform.to_json()

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/platforms/<int:id>", methods=["DELETE"])
def delete_platform(id: int) -> str:
    status_code: int = 202
    content: str = ""

    platform: Platform = Platform.query.get(id)
    if platform is None:
        status_code = 500
        content = (
            f'{{"success":false,"message":"Could not find platform with ID {id}"}}'
        )
    else:
        db.session.delete(platform)
        db.session.commit()
        content = f'{{"success":true,"message":"Deleted platform with ID {id}"}}'

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/schema", methods=["GET"])
def get_schema() -> str:
    status_code: int = 200
    content: str = ""

    try:
        content = get_schema_from_file()
    except:
        status_code = 204
        content = ""

    response = make_response(content, status_code)
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True)
