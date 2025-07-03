from subprocess import check_output

from loggingSettings import logger_wrapper

class IPScanner():
    
    def __init__(self, port, ip_range, regex_ip_filter):
        self.port = port
        self.ip_range = ip_range
        self.regex_ip_filter = regex_ip_filter

    
    @logger_wrapper   
    def scan_ips(self):
        command = f"nmap -sT -p {self.port} "\
            f"{self.ip_range} | grep -oP '{self.regex_ip_filter}'"

        command_result = check_output((command), shell=True).decode()
        
        return list(filter(lambda i: i != '', 
                           command_result.split('\n')))
        