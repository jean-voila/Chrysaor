---

# Chrysaor
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fjean-voila%2FChrysaor&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

Chrysaor is an unofficial Python API for accessing academic data from the *Pegasus* service provided by the *IONIS* school group. This API allows students and parents to programmatically access their grades and academic information using reverse engineering techniques, including requests (using the `requests` module) and web scraping with `BeautifulSoup`.


## Setup

To use Chrysaor, ensure you have Python 3.6 or later installed. Clone the repository and install dependencies:

```bash
git clone https://github.com/jean-voila/Chrysaor.git
cd Chrysaor
pip install -r requirements.txt
```

## Usage

1. **Setup Credentials**: Ensure your `credentials` file in the `data` directory contains your Pegasus login details.
    Here is an example of the credential file :
    ```
    john.smith
    zivEI34sv
    ```
2. **Run Example Script**:

   ```bash
   python main.py
   ```

   This script initializes an instance of `PegasusData`, logs into Pegasus using credentials, and retrieves student information. It scans the existence and validity of the `cookie` file in the `data` folder. If it's empty or invalid, `PegasusData` will automatically create/update and store it. Then the raw data will be fetched. 

3. **Integrate into Your Project**: Import `StudentLogging` and use its functions to authenticate and retrieve data. See `main.py` for an example implementation.

## Example Code (main.py)

```python
import StudentLogging

class PegasusData():
    def __init__(self):
        self.success = False
        self.cookie  = ""
        self.name    = ""

    def __GetData__(self, credentialFile="data/credentials", cookieFile="data/cookie", verboseOutput=True):
        loggingData = StudentLogging.log(credentialFile, cookieFile, verboseOutput)
        self.success = bool(loggingData["success"])
        self.cookie  = loggingData["cookie"]
        self.name    = loggingData["name"]

# Example usage:
studentData = PegasusData()
studentData.__GetData__()
print(f"Logged in as: {studentData.name}")
```

## License

This project is licensed under the [Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/) license. See the [LICENSE.txt](LICENSE.txt) file for more details.

## Disclaimer

Chrysaor is an independent project and is not officially affiliated with or endorsed by the IONIS school group or the Pegasus service.

---
