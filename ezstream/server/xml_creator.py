import os.path
from dataclasses import dataclass
from mount import Mount


@dataclass(frozen=True)
class XMLCreator:

    mount: Mount
    __base_path: str = r'/ezstream'
    # __base_path: str = r'/home/ilya/git/radio_tools/ezstream'

    @classmethod
    def create(cls, mount: int):
        return cls(Mount.from_int(mount)).__create()

    @property
    def __filepath(self):
        return os.path.join(self.__base_path, f'ezstream_{self.mount.value}.xml')

    def __create(self):
        with open(self.__filepath, 'w', encoding='utf-8') as file:
            file.write(self.__content)

    @property
    def __content(self):
        return f"""<ezstream>
    <servers>
        <server>
            <name>main</name>
            <protocol>HTTP</protocol>
            <hostname>icecast</hostname>
            <port>800{self.mount.int}</port>
            <user>source</user>
            <password>admin</password>
            <tls>May</tls>
            <tls_cipher_suite>HIGH:!RSA:!SHA:!DH:!aNULL:!eNULL:!TLSv1</tls_cipher_suite>
        </server>
    </servers>
    <streams>
        <stream>
            <stream_name>main</stream_name>
            <mountpoint>/stream_{self.mount.value}</mountpoint>
            <intake>mount</intake>
            <server>main</server>
            <format>MP3</format>
            <stream_url>http://icecast:800{self.mount.int}/stream_{self.mount.value}</stream_url>
        </stream>
    </streams>
    <intakes>
        <intake>
            <name>mount</name>
            <type>playlist</type>
            <filename>/ezstream/playlist_{self.mount.value}.txt</filename>
        </intake>
    </intakes>
</ezstream>"""
