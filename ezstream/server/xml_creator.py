import os.path
from mount import Mount


class XMLCreator:

    mount: Mount
    __base_path = r'/ezstream'

    @classmethod
    def create(cls, mount: Mount):
        with open(cls.__filepath(mount), 'w', encoding='utf-8') as file:
            file.write(cls.__content(mount))

    @classmethod
    def __filepath(cls, mount: Mount):
        return os.path.join(cls.__base_path, f'ezstream_{mount.value}.xml')

    @staticmethod
    def __content(mount: Mount):
        return f"""
<ezstream>
    <servers>
        <server>
            <name>main</name>
            <protocol>HTTP</protocol>
            <hostname>icecast</hostname>
            <port>800{mount.int}</port>
            <user>source</user>
            <password>admin</password>
            <tls>May</tls>
            <tls_cipher_suite>HIGH:!RSA:!SHA:!DH:!aNULL:!eNULL:!TLSv1</tls_cipher_suite>
        </server>
    </servers>
    <streams>
        <stream>
            <stream_name>main</stream_name>
            <mountpoint>/stream_{mount.value}</mountpoint>
            <intake>mount</intake>
            <server>main</server>
            <format>MP3</format>
            <stream_url>http://icecast:800{mount.int}/stream_{mount.value}</stream_url>
        </stream>
    </streams>
    <intakes>
        <intake>
            <name>mount</name>
            <type>playlist</type>
            <filename>/ezstream/playlist_{mount.value}.txt</filename>
        </intake>
    </intakes>
</ezstream>"""
