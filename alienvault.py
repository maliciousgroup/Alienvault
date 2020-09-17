import json
import sys

from utils.colors import colors
from utils.output import write_to_file
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

ansi = colors()


class Alienvault:

    def __init__(self, _domain: str, _apikey: str, _output: str):
        self.domain = _domain
        self.apikey = _apikey
        self.output = _output
        self.get_otx_data(self.domain, self.apikey, self.output)

    @staticmethod
    def get_otx_data(_dom: str, _apikey: str, _output: str = ''):

        page: int = 1
        headers: dict = {'X-OTX-API-KEY': f'{apikey}'}

        while True:
            link = f"https://otx.alienvault.com/api/v1/indicators/hostname/{_dom}/url_list?matchType=prefix&page={page}"

            with Session() as session:
                retry = Retry(connect=2, backoff_factor=0.25, status_forcelist=[429, 504])
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter=adapter)
                session.mount('https://', adapter=adapter)
                response_data = session.get(link, headers=headers).text
                data_json = json.loads(response_data)
                for key in data_json['url_list']:
                    print(key['url'])
                    if _output:
                        write_to_file(_output, key['url'] + '\n')
                if str(data_json['has_next']).lower() == 'true':
                    page += 1
                    continue
                else:
                    break


def banner() -> None:
    _output: str = f"""{ansi['red']}

 █████╗ ██╗     ██╗███████╗███╗   ██╗██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██╔══██╗██║     ██║██╔════╝████╗  ██║██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
███████║██║     ██║█████╗  ██╔██╗ ██║██║   ██║███████║██║   ██║██║     ██║   
██╔══██║██║     ██║██╔══╝  ██║╚██╗██║╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   
██║  ██║███████╗██║███████╗██║ ╚████║ ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   
╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   
                                            
                                            Written by d3d (@MaliciousGroup)  
                                            Version 1.1   {ansi['reset']}
    """
    print(_output)


def usage() -> None:
    _output: str = f"""{ansi['bold']}
      '-d', '--domain'      - (Optional) Set a domain to gather URL(s)
      '-k', '--apikey'      - (Optional) Set the AlienVault API key
      '-o', '--output'      - (Optional) Set the output file for writing 
    {ansi['reset']}
    """
    print(_output)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(add_help=True, usage=usage)
    parser.add_argument('-d', '--domain', action='store', dest='domain', required=True)
    parser.add_argument('-k', '--apikey', action='store', dest='apikey', required=False)
    parser.add_argument('-o', '--output', action='store', dest='output', required=False)
    arg = None
    try:
        banner()
        arg = parser.parse_args()
    except TypeError:
        usage()
        sys.exit(f"{ansi['red']}Invalid OR missing required option. Exiting.{ansi['reset']}\n")
    domain = arg.domain if arg.domain else None
    output = arg.output if arg.output else ''
    apikey = arg.apikey if arg.apikey else ''

    obj = Alienvault(domain, apikey, output)
