import numpy as np


headers = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
            "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
            "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_hot_login",
            "is_guest_login", "count", "srv_count", "serror_rate", "srv_error_rate", "rerror_rate", "srv_rerror_rate",
            "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
            "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
            "dst_host_srv_rerror_rate", "label", "difficulty_inverse"]

features = headers[:-2]
target = ["label"]


protocols = ['tcp', 'udp', 'icmp']

services = ['ftp_data', 'other', 'private', 'http', 'remote_job', 'name', 'netbios_ns', 'eco_i', 'mtp', 'telnet',
            'finger', 'domain_u', 'supdup', 'uucp_path', 'Z39_50', 'smtp', 'csnet_ns', 'uucp', 'netbios_dgm',
            'urp_i', 'auth', 'domain', 'ftp', 'bgp', 'ldap', 'ecr_i', 'gopher', 'vmnet', 'systat', 'http_443',
            'efs', 'whois', 'imap4', 'iso_tsap', 'echo', 'klogin', 'link', 'sunrpc', 'login', 'kshell', 'sql_net',
            'time', 'hostnames', 'exec', 'ntp_u', 'discard', 'nntp', 'courier', 'ctf', 'ssh', 'daytime', 'shell',
            'netstat', 'pop_3', 'nnsp', 'IRC', 'pop_2', 'printer', 'tim_i', 'pm_dump', 'red_i', 'netbios_ssn',
            'rje', 'X11', 'urh_i', 'http_8001', 'aol', 'http_2784', 'tftp_u', 'harvest']

flags = ['SF', 'S0', 'REJ', 'RSTR', 'SH', 'RSTO', 'S1', 'RSTOS0', 'S3', 'S2', 'OTH']

categorical_feature_list = ["protocol_type", "service", "flag"]
categories_list = [protocols, services, flags]

# Classes of attacks
"""
labels = ['normal', 'neptune', 'warezclient', 'ipsweep', 'portsweep', 'teardrop', 'nmap', 'satan', 'smurf', 'pod',
           'back', 'guess_passwd', 'ftp_write', 'multihop', 'rootkit', 'buffer_overflow', 'imap', 'warezmaster', 'phf',
           'land', 'loadmodule', 'spy', 'perl', 'saint', 'mscan', 'apache2', 'snmpgetattack', 'processtable',
           'httptunnel', 'ps', 'snmpguess', 'mailbomb', 'named', 'sendmail', 'xterm', 'worm', 'xlock', 'xsnoop',
           'sqlattack', 'udpstorm']
"""

labels = ['BENIGN', 'Heartbleed', 'Bot', 'Web Attack � Brute Force', 'FTP-Patator', 'PortScan', 'DoS Slowhttptest',
          'DoS Hulk', 'Infiltration', 'DoS slowloris', 'Web Attack � Sql Injection', 'DDoS', 'SSH-Patator',
          'DoS GoldenEye', 'Web Attack � XSS']

classes = [i for i in range(len(labels))]

# Base Truth configuration
truth_size = 20000
truth_update_frac = 0.10
threshold_percentile = 40
truth_save_folder = "./detection/outlier/truth/save_state/"

outlier_save_folder = "./detection/outlier/save_state/"
classifier_save_folder = "./detection/classification/save_state/"

head = {' Fwd IAT Max', ' Bwd Avg Bytes/Bulk', ' Flow Packets/s', ' Packet Length Variance', 'FIN Flag Count',
        ' Average Packet Size', 'Flow Bytes/s', ' Max Packet Length', ' Flow IAT Mean', ' Flow IAT Min', ' Bwd PSH Flags',
        'Fwd PSH Flags', ' Packet Length Std', ' RST Flag Count', ' Subflow Fwd Bytes', ' Avg Bwd Segment Size', ' Idle Std',
        ' Flow Duration', ' Bwd IAT Std', 'Total Length of Fwd Packets', 'Fwd Avg Bytes/Bulk', ' ECE Flag Count',
        ' act_data_pkt_fwd', ' Active Std', ' Idle Max', ' Min Packet Length', ' Flow IAT Max', 'Active Mean', 'Idle Mean',
        ' Active Min', ' Fwd Packet Length Mean', ' PSH Flag Count', ' Subflow Bwd Packets', ' Fwd Avg Packets/Bulk',
        ' Bwd Packet Length Std', ' Packet Length Mean', 'Init_Win_bytes_forward', ' URG Flag Count', ' Total Length of Bwd Packets',
        ' Total Backward Packets', 'Bwd Avg Bulk Rate', ' min_seg_size_forward', ' Active Max', ' Bwd IAT Mean', ' Fwd Header Length.1',
        ' Total Fwd Packets', ' Bwd Packet Length Min', ' Destination Port', ' ACK Flag Count', ' Fwd Packet Length Std',
        ' Fwd IAT Std', ' Bwd Packet Length Mean', ' Fwd Avg Bulk Rate', ' Bwd Header Length', 'Subflow Fwd Packets',
        ' Idle Min', ' Fwd Packet Length Min', ' Bwd URG Flags', ' Down/Up Ratio', ' Flow IAT Std', 'Bwd Packet Length Max',
        ' Fwd IAT Min', ' Init_Win_bytes_backward', ' Bwd IAT Min', ' SYN Flag Count', ' Bwd IAT Max', ' Bwd Avg Packets/Bulk',
        ' Subflow Bwd Bytes', ' Avg Fwd Segment Size', ' Label', ' CWE Flag Count', ' Fwd Packet Length Max', 'Bwd IAT Total',
        ' Fwd Header Length', 'Fwd Packets/s', ' Bwd Packets/s', 'Fwd IAT Total', ' Fwd IAT Mean', ' Fwd URG Flags'}

dtypes = {k: np.float64 for k in head}
dtypes[' Label'] = str