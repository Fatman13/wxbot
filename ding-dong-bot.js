/**
 * Wechaty - WeChat Bot SDK for Personal Account, Powered by TypeScript, Docker, and 💖
 *  - https://github.com/chatie/wechaty
 */
const {
  Wechaty,
  ScanStatus,
  log,
} = require('wechaty')

/**
 * You can ignore the next line becasue it is using for CodeSandbox
 */
require('./.util/helper')

const fastcsv = require('fast-csv');
const fs = require('fs');

const ObjectsToCsv = require('objects-to-csv')

let res = new Object()

function onScan (qrcode, status) {
  if (status === ScanStatus.Waiting || status === ScanStatus.Timeout) {
    require('qrcode-terminal').generate(qrcode, { small: true })  // show qrcode on console

    const qrcodeImageUrl = [
      'https://api.qrserver.com/v1/create-qr-code/?data=',
      encodeURIComponent(qrcode),
    ].join('')

    log.info('StarterBot', 'onScan: %s(%s) - %s', ScanStatus[status], status, qrcodeImageUrl)

  } else {
    log.info('StarterBot', 'onScan: %s(%s)', ScanStatus[status], status)
  }
}

function onLogin (user) {
  log.info('StarterBot', '%s login', user)
}

function onLogout (user) {
  log.info('StarterBot', '%s logout', user)
}

async function onMessage (msg) {
  log.info('StarterBot', msg.toString())
  const from_contact = msg.from()
  const to_contact = msg.to()
  const text = msg.text()
  const room = msg.room()
  log.info('StarterBot', 'from: %s, text: %s, room: %s', from_contact, text, room)
  const msg_date = msg.date()
  let chat_name = null
  if (room){
    const topic = await room.topic()
    chat_name = topic.toString()
  } else {
    if (from_contact.toString().includes('Yu@Tenjin')){
      chat_name = to_contact.toString()
    } else {
      chat_name = from_contact.toString()
    }
  }

  if (!(chat_name in res)){
    res[chat_name] = new Object()
    res[chat_name]['messages'] = []
    res[chat_name]['tag'] = null
    res[chat_name]['1st_responded_at'] = null 
    res[chat_name]['jira_ticket_no'] = null 
    res[chat_name]['ended_at'] = null 
    res[chat_name]['started_at'] = msg_date.toString()
  }
  let new_msg_entry = new Object()
  new_msg_entry['from'] = from_contact.toString()
  new_msg_entry['text'] = text.toString()
  new_msg_entry['date'] = msg_date.toString()
  res[chat_name]['messages'].push(new_msg_entry)

  if ((from_contact.toString().includes('Yu@Tenjin') 
      || from_contact.toString().includes('Ming') 
      || from_contact.toString().includes('Fatman13')) 
      && (text.toString().includes('sup')
      || text.toString().includes('[握手]'))) {
    log.info('StarterBot', 'Logging customer support conversation... ')
    if (from_contact.toString().includes('Fatman13') && text.toString().includes('sup')) {
      const coms = text.toString().split(' ')
      const n_index = coms.indexOf('-n')
      if (n_index != -1 && coms[n_index+1] != -1) {
        chat_name = coms[n_index+1].replace(/_/g, ' ')
        log.info('StarterBot', 'Changing chat_name to %s', chat_name) 
      }
    }

    let data = new Object()
    data['started_at'] = res[chat_name]['started_at']
    data['ended_at'] = msg_date.toString()
    data['name'] = chat_name
    data['1st_responded_at'] = null
    data['tag'] = null
    data['jira_ticket_no'] = null 
    data['logged_by'] = from_contact.toString()
    data['messages'] = JSON.stringify(res[chat_name]['messages'])

    const coms = text.toString().split(' ')
    const t_index = coms.indexOf('-t')
    if (t_index != -1 && coms[t_index+1] != -1) {
      data['tag'] = coms[t_index+1]
    }
    const j_index = coms.indexOf('-j')
    if (j_index != -1 && coms[j_index+1] != -1) {
      data['jira_ticket_no'] = coms[j_index+1]
    }
    const c_index = coms.indexOf('-c')
    if (c_index != -1 && coms[c_index+1] != -1) {
      data['name'] = coms[c_index+1]
    }

    for (let ent of res[chat_name]['messages']){
      // log.info('StarterBot', 'messages loop ent: %s', ent)
      // When message got recalled, 
      // a random number string will showup as a text
      // try to negate that by the following
      if (/^\d+$/.test(ent['text'])){
        continue
      }

      if (ent['from'].includes('Yu@Tenjin') || ent['from'].includes('Ming')){
        data['1st_responded_at'] = ent['date']
        break
      }
    }

    delete res[chat_name]

    const file_name = 'cn_sup_' + (new Date()).toISOString().replace(/\..+/, '') + '.csv'
    const file_path = ([ __dirname, '../log', file_name]).join('/')
    log.info('StarterBot', 'Writting to %s', file_path)    

    const csv = new ObjectsToCsv([data])
    await csv.toDisk(file_path)

    // const wstream = fs.createWriteStream(file_path)
    // fastcsv
    //   .write(data, { headers: true })
    //   .pipe(wstream)
  }
}

const bot = new Wechaty({
  name: 'ding-dong-bot',
  /**
   * Specify a puppet for a specific protocol (Web/Pad/Mac/Windows, etc).
   *
   * You can use the following providers:
   *  - wechaty-puppet-hostie
   *  - wechaty-puppet-puppeteer
   *  - wechaty-puppet-padplus
   *  - wechaty-puppet-macpro
   *  - etc.
   *
   * Learn more about Wechaty Puppet Providers at:
   *  https://github.com/wechaty/wechaty-puppet/wiki/Directory
   */
  // puppet: 'wechaty-puppet-wechat4u',
  // Set as above, or set using environment variable WECHATY_PUPPET
})

bot.on('scan',    onScan)
bot.on('login',   onLogin)
bot.on('logout',  onLogout)
bot.on('message', onMessage)

bot.start()
  .then(() => log.info('StarterBot', 'Starter Bot Started.'))
  .catch(e => log.error('StarterBot', e))
