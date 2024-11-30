import ftplib
import json
import io

def upload_json(data_dict, remote_filename):
    """
    Upload a JSON from a dictionary directly to FTP server
    
    :param data_dict: Dictionary to be uploaded as JSON
    :param remote_filename: Filename to use on the FTP server
    """
    FTP_SERVER = 'localhost'  
    FTP_PORT = 21
    FTP_USER = 'testuser'
    FTP_PASS = 'testpass'

    try:
        with ftplib.FTP() as ftp:
            ftp.connect(host=FTP_SERVER, port=FTP_PORT)
            
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            
            json_data = json.dumps(data_dict, indent=4)
            
            json_file = io.BytesIO(json_data.encode('utf-8'))
            
            ftp.storbinary(f'STOR {remote_filename}', json_file)
            
            print(f"Successfully uploaded JSON to {remote_filename}")

    except ftplib.all_errors as e:
        print(f"FTP error occurred: {e}")

if __name__ == '__main__':
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "projects": [
            "Web Development",
            "Data Analysis"
        ]
    }
    
    upload_json(sample_data, 'user_data.json')
