from urllib.parse import unquote, quote


class ParseHeader:
    def __init__(self, text):

        self.text = text
        self.method = text.split()[0]
        self.path = text.split()[1]
        self.body = text.split('\r\n\r\n', 1)[1]

    def form_body(self):
        return self._parse_parameter(self.body)

    def parse_path(self):
        index = self.path.find('?')
        if index == -1:
            return self.path, {}
        else:
            path, query_string = self.path.split('?', 1)
            query = self._parse_parameter(query_string)
            return path, query

    @property
    def headers(self):
        header_content = self.text.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        result = {}
        for line in header_content:
            k, v = line.split(': ')
            result[quote(k)] = (v)
        return result

    @staticmethod
    def _parse_parameter(parameters):
        args = parameters.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = unquote(v)
        return query


from tomura.decoder import get_decoder

class ParseConetet:
    def __init__(self, items):
        try:
            text = str(items, 'utf-8', errors='ignore')
        except (LookupError, TypeError):
            text = str(items, errors='ignore')
        self.contents = items

        self._headers = ParseHeader(text)
        self.headers = self._headers.headers
        self.method = self._headers.method
        self.path,self.params= self._headers.parse_path()

    @property
    def body(self):
        # print(self.headers)
        content_type = self.headers.get('Content-Type',None)
        transfer_encoding  = self.headers.get('Transfer-Encoding',None)
        content_encoding = self.headers.get('Content-Encoding',None)
        contents = self._body_content()
        try:
            if (contents):
                if transfer_encoding == 'chunked':
                    body_content = self._chunked_body(contents)
                else:
                    body_content = contents
                if content_encoding:
                    return get_decoder(content_encoding).decompress(body_content)
                return body_content
        except:
            pass
        return contents


    def _get_index(self, content, partten):
        for i in range(len(content)):
            #   print(content[i:i + 4])
            if (content[i:i + len(partten)]) == partten:
                return i + len(partten)
        return 0

    def _body_content(self):
        # print(self.content)
        length = self._get_index(self.contents, b'\r\n\r\n')
        body_content = self.contents[length:]
        return body_content

    def _chunked_body(self,content):
        body_content = b''
        while 1:
            try:
              #  print(content)
                index = self._get_index(content, b'\r\n') - 2
                if index <= 0:
                    break
                count = int(content[:index].decode('utf-8'), 16)
                if (count == 0):
                    break
                body_content = body_content + content[index + 2:count + index + 2]
                content = content[count + index + 2 + 2:]
            except:
                break
        return body_content

    @property
    def html(self):
        try:
            return self.body.decode('utf-8')
        except:
            return None


