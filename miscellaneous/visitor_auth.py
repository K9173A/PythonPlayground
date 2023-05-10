import hashlib
import hmac
import json
import uuid
from typing import Dict, Optional


class VisitorHashCalculator:

    def __init__(self, hash_algorithm: str, private_key: str) -> None:
        self._hash_algorithm = hash_algorithm
        self._private_key = private_key

    def get_visitor_ext(self, fields: Dict, expires: Optional[int] = None) -> str:
        visitor_hash = self.get_provided_visitor_hash(fields=fields, expires=expires)

        return json.dumps({
            'hash': visitor_hash,
            'fields': fields,
            'expires': expires
        })

    def get_provided_visitor_hash(self, fields: Dict, expires: Optional[int] = None) -> str:
        msg_parts = [fields[key] for key in sorted(fields.keys())]

        if expires:
            msg_parts.append(str(expires))

        msg = ''.join(msg_parts).encode('utf-8')

        if self._hash_algorithm == 'hmac-sha256':
            return hmac.new(
                key=self._private_key.encode(),
                msg=msg,
                digestmod=hashlib.sha256
            ).hexdigest()

        else:
            if self._hash_algorithm == 'sha256':
                hash_function = hashlib.sha256()
            elif self._hash_algorithm == 'md5':
                hash_function = hashlib.md5()
            else:
                raise ValueError(f'Unsupported hash algorithm {self._hash_algorithm}')

            hash_function.update(msg)
            hash_function.update(self._private_key.encode())

            return hash_function.hexdigest()


def main() -> None:
    visitor_hash_calculator = VisitorHashCalculator(
        hash_algorithm='md5',
        private_key='1234'
    )

    result = visitor_hash_calculator.get_visitor_ext(
        fields={
            'phone': '+79998887766',
            'display_name': 'Peter',
            'id': str(uuid.uuid4()),
            'email': 'peter@test.com'
        },
        expires=1681195621  # Tuesday, April 11, 2023 6:47:01 AM
    )

    print(result)


if __name__ == '__main__':
    main()
