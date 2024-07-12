# AutoPyKey

## History
A very interesting and useful one-day project that has grown into a full-fledged program / script.

It was originally conceived to automate the creation of accounts for twitch drops, but it has grown into something more.

## Usage
1. Always edit the `run.bat` file after installation or update according to the help message from running `AutoPyKey.py`
   ![image](https://github.com/user-attachments/assets/e52d6151-bc7c-41a6-8057-7b508e03d1a6)
2. Install or update the libraries with `python -m pip install pyautogui pynput keyboard`
3. When running the record modes you need to know these controls:
   * `[Record] start/end` - means the record process has started/ended;
   * `[Step] start/end` - means the step process has started/ended;
   * When the record and step is running you can change the parameters of the step wich include:
     * pressing `1` - adding _a click_ to the step;
     * pressing `2` - adding _writing a login_ to the step;
     * pressing `3` - adding _writing a password_ to the step;
     * pressing `4` - adding _pressing ctrl+c_ to the step;
     * pressing `5` - adding _pressing ctrl+v_ to the step;
   * Pressing `space` is ending the choosing of the parameters, saving the position of the cursor and ending the step;
   * Pressubg `esc` does the same but also ends the record process.
4. When running other modes you don't need to do anything other than running the `run.bat` file.

## Bonus usage
When running in `rW` mode it writes the script to a file instead of running it, but when running in `Rp` mode it reads the script file and plays it.

But instead of running exitsting file as is you can change it, the syntax is easy: `stepid|pointX,pointY|globalTimeInSeconds|toClick,toWriteLogin,toWritePassword,toCopy,toPaste`.
