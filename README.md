
# Sage SDK

A Python package to authenticate, fetch, post, validate, and process Sage data.

## Features

- authenticate with sage.
- fetch data from sage.
- post data to sage.
- validate posted data to sage.
- process validated data in sage.

## Installation

To install the Sage SDK, follow these steps:

1. have python 3.9+ installed
2. run the follwing command

   ```
   pip install sage-sdk
   ```
## Usage
1. from sage_sdk import connection:

   ```
  from sage_sdk import Client
  
  host = "hostname"
  username = "username"
  password = "password"
  api_key = "api_key"
  endpoint = "endpoint"
  
  client = Client(host, username, password, api_key)
  data = client.get_data(endpoint)
  #use the data
  
   
   ```


## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue on GitHub or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.