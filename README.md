# dir-watcher

## How to run
To run as a container
1) Edit the `app.env`

```
TZ=Asia/Seoul
NOTIFICATION=telegram
DIR_TO_WATCH=DIR1,DIR2,...
TELEGRAM_API_TOKEN=FIXME
TELEGRAM_CHAT_ID=FIXME
```

* `NOTIFICATION` : `telegram` or `none`
* `DIR_TO_WATCH` : full-path of directories to watch in commma-separated

2) `make run`


## Example 
```
TZ=Asia/Seoul
NOTIFICATION=telegram
DIR_TO_WATCH=/tmp, /etc
TELEGRAM_API_TOKEN=123
TELEGRAM_CHAT_ID=456
```
