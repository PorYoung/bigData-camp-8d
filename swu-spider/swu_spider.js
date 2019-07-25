const util = require('util');
const readline = require('readline');
const Readable = require('stream').Readable;
const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');
const appendFile = util.promisify(fs.appendFile);
const writeFile = util.promisify(fs.writeFile);

const requests = axios.create({ baseURL: 'http://222.198.125.159' });

async function main() {
  await writeFile(
    'summary.csv',
    ['title', 'category', 'speaker', 'date', 'url', 'times'].join('\t') + '\n',
    'utf-8'
  );
  for (let i = 1; i < 35; i++) {
    console.log(`正在获取第${i}页的数据……`);
    const { data } = await requests.get(
      `/seeyon/xndxNewsData.do?method=getBoardMoreList&curPage=${i}&typeId=8295600936326352000pageSize=35`
    );
    const $ = cheerio.load(data);
    $('div.list-box>ul li').each(async function(index, elem) {
      const eleT = $(this).text();
      let match = eleT.match(/^(\d{4}-\d{2}-\d{2})【([^【】]{4})】(.*)$/);
      const [, date, category, title] = match
        ? match
        : [null, null, null, null];
      const url = $(this)
        .find('a')
        .attr('onclick')
        .slice(9, -2);
      let { data } = await requests.get(url);
      data = data.replace(/&nbsp;/g, ' ');
      const rlin = new Readable();
      rlin.push(data);
      rlin.push(null);
      let speaker = '';
      let nextLineQ = false;
      const rl = readline.createInterface({
        input: rlin
      });
      rl.on('line', ipu => {
        if (nextLineQ == true) {
          speaker = ipu.split(/，|,/)[0].trim();
          rl.close();
          return;
        }
        if (
          /((主\s*讲\s*人)|(演\s*讲\s*人)|(报\s*告\s*人)|(讲\s*座\s*人)|(讲座嘉宾)|(报告嘉宾)|(演讲嘉宾)|(主讲嘉宾))：/.test(
            ipu
          )
        ) {
          const $_$ = ipu.replace(/<[^<>]*?>/g, '');
          // console.log($_$);
          match = $_$.match(
            /((主\s*讲\s*人：)|(演\s*讲\s*人：)|(报\s*告\s*人：)|(讲\s*座\s*人：)|(讲座嘉宾：)|(报告嘉宾：)|(演讲嘉宾：)|(主讲嘉宾：))(.+)/
          );
          if (match == null) {
            nextLineQ = true;
            return;
          }
          speaker = match[10];
          rl.close();
        }
      });
      rl.once('close', async () => {
        nextLineQ = false;
        match = data.match(/阅读次数:(\s+)?(\d+)(\s+)?<\/td>/);
        const times = match && match[2];
        speaker = speaker.trim();
        const listArray = [title, category, speaker, date, url, times];
        // 清洗数据
        for (let j = 0; j < listArray.length; j++) {
          const v = listArray[j];
          if (/^\s*$/.test(v)) {
            return;
          }
        }
        // 写入统计表
        await appendFile('summary.csv', listArray.join('\t') + '\n', 'utf-8');
        const $$ = cheerio.load(data);
        const text = $$('#content').text();
        // 写入文件
        if (date) {
          await appendFile(
            // 按相同月份写入同一个文件
            date.slice(0, -3) + '.txt',
            text + '\n======\n',
            'utf-8'
          );
        }
      });
    });
    // 有点累了，休息1秒
    await sleep(1000);
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

main();
