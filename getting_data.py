"""
THIS IS MEANT AS A DEMO FOR SOMEONE WHO IS UNFAMILIAR WITH THE DATASETS FOR PROJECT ARIAS


"""

import json 
import requests
import scriptconfig as scfg
import ubelt as ub
import kwutil
import os.path

class getting_dataCLI(scfg.DataConfig):
    file_path = scfg.Value('/home/vinnie/code/aria_playground/Nymeria_download_urls.json', help = "Provide a json file to read data")

    out_fpath = scfg.Value('/home/vinnie/Desktop/nymera_res', help = "Provide location for data outputted")

    workers = scfg.Value(4 ,  help="Describe number of workers for downloading files")
    
    num_sequences = scfg.Value(0, help="Get number of sequences based on number described if 0 is picked then it will download all sequences")

def get_sequence_assest(filename, download_url):
    if not os.path.isfile(filename):
        response = requests.get(download_url)
        if response.status_code == 200:  # Check if the request was successful
            with open(filename, 'wb') as file:
                file.write(response.content)
        else:
            print("No file downloaded")
    else:
        print('already downloaded moving on')




def main():
    """
    IGNORE:
    from getting_data import *
    config = {
    'file_path' : '/home/vinnie/code/aria_playground/Nymeria_download_urls.json',

    'out_fpath' : '/home/vinnie/Desktop/nymera_res',
    }

    """

    config = getting_dataCLI.cli(cmdline=True, special_options=False)
    with open(config['file_path']) as f:
        data = json.load(f)

    dpath = ub.Path(config['out_fpath']).ensuredir()


    #DATA IS DIVIDED INTO SEVERAL SEQUENCES EACH OF WHICH CONTAINING UNIQUE DATA
    # WE ASSUME YOU HAVE THE MAIN JSON FILE PROVIDED FROM THIS LINK:
    # https://www.projectaria.com/datasets/nymeria/ 




    #The following items are avalable in this
    num_sequences = config['num_sequences'] 
    count = 0
    pman = kwutil.ProgressManager()
    pool  = ub.JobPool('thread', max_workers=config['workers'])


    with pman:
        for k in data['sequences'].keys():
            sequence = data['sequences'][k]
            dpath_seq = (dpath / k).ensuredir()
            count_k2=0
            if count <= num_sequences :
                for k_2 in sequence.keys():
                    filename =  dpath_seq /  sequence[k_2]['filename']
                    download_url = sequence[k_2]['download_url']
                    pool.submit(get_sequence_assest,filename,download_url)
                    count_k2+=1
                job_prog = pman.progiter(pool.as_completed(desc='downloading...'),total=count_k2)
                for job in job_prog:
                    ...
                
            count+=1

    #print(sequence.keys())


if __name__ == "__main__":
    main()