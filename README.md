# EVM Wallet Scanner

This software scans seed phrases to find associated wallet addresses and their balances on Ethereum, Polygon, and Binance Smart Chain (BSC).

## Instructions to use the Software

1. **Download Git on your system**:
   - First, check if Git is installed in your system by typing this: `git --version` in your command prompt. If you get an output like this `git version 2.45.1` then Git is already installed in your system.
   - If you get an output like this `git is not recognized` or `git --version` then download Git from the following URL and again run the command `git --version` to ensure if it has been downloaded or not:
    ```sh
    https://git-scm.com/download/
    git --version
    ```
2. **Clone the Repository**:
    ```sh
    git clone https://github.com/pikaimandal/evm.git
    cd evm_wallet_scanner
    ```    

2. **Run the Setup Script**:
    - Open the command prompt and navigate to the `evm_wallet_scanner` directory if you aren't already there.
        ```sh
        cd evm_wallet_scanner
        ```
    - Run the setup script:
        ```sh
        setup.bat
        ```
    - Alternatively, you can double-click the `setup.bat` file in the File Explorer to run it.

The script will guide you through the process of installing Python (if not already installed), setting up a virtual environment, installing dependencies, and running the software.

## License

This project is licensed under the MIT License.
