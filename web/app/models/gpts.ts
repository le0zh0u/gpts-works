// import { QueryResultRow, sql } from "@vercel/postgres";
import mysql from 'mysql2/promise';
import { RowDataPacket } from 'mysql2';
import { Gpts } from "@/app/types/gpts";
import { isGptsSensitive } from "@/app/services/gpts";

const dbConfig = {
  host: process.env.DB_HOST,
  port: process.env.DB_PORT ? parseInt(process.env.DB_PORT, 13306) : 3306,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
};

const pool = mysql.createPool(dbConfig);

export async function createTable() {
  const res = await pool.execute(`CREATE TABLE gpts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(50) UNIQUE NOT NULL,
    org_id VARCHAR(50),
    name VARCHAR(50),
    description TEXT,
    avatar_url VARCHAR(255),
    short_url VARCHAR(100),
    author_id VARCHAR(50),
    author_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    welcome_message VARCHAR(512),
    tools VARCHAR(255),
    prompt_starters VARCHAR(2048),
    detail JSON 
);`);

  return res;
}

export async function insertRow(gpts: Gpts) {
  // 使用参数化查询
  const [res] = await pool.execute(`
    INSERT INTO gpts 
    (uuid, org_id, name, description, avatar_url, short_url, author_id, author_name, created_at, updated_at, welcome_message, detail) 
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `, [
    gpts.uuid, 
    gpts.org_id, 
    gpts.name, 
    gpts.description, 
    gpts.avatar_url, 
    gpts.short_url, 
    gpts.author_id, 
    gpts.author_name, 
    gpts.created_at, 
    gpts.updated_at, 
    gpts.welcome_message,
    JSON.stringify(gpts.detail) // 确保 detail 是 JSON 字符串
  ]);

  return res;
}

export async function getUuids(): Promise<string[]> {
  const [rows] = await pool.execute(`SELECT uuid FROM gpts`) as RowDataPacket[];
   // 使用 rows.length 来判断行数
   if (rows.length === 0) {
    return [];
  }

  let uuids: string[] = [];
  rows.forEach((row:RowDataPacket) => {
    uuids.push(row.uuid);
  });

  return uuids;
}

export async function getRows(last_id: number, limit: number): Promise<Gpts[]> {
  const [rows] =
    await pool.execute(`SELECT * FROM gpts WHERE id > ? LIMIT ?`, [last_id, limit]) as RowDataPacket[];

  if (rows.length === 0) {
    return [];
  }

  const gpts: Gpts[] = [];
  
  rows.forEach((row:RowDataPacket) => {
    const gpt = formatGpts(row);
    if (gpt) {
      gpts.push(gpt);
    }
  });

  return gpts;
}

// export async function getRandRows(last_id: number, limit: number): Promise<Gpts[]> {
  
//   const [rows] = await pool.execute(`SELECT * FROM gpts WHERE id > ${last_id} ORDER BY RAND() LIMIT ${limit}`) as RowDataPacket[];
//   // 使用 rows.length 来判断行数
//   if (rows.length === 0) {
//     return [];
//   }

//   const gpts: Gpts[] = [];

//   rows.forEach((row:RowDataPacket) => {
//     const gpt = formatGpts(row);
//     gpts.push(gpt);
//   });

//   return gpts;
// }

export async function getRandRows(
  last_id: number,
  limit: number
): Promise<Gpts[]> {
  const [rows] = await pool.execute(`SELECT * FROM gpts WHERE id > ${last_id} ORDER BY RAND() LIMIT ${limit}`) as RowDataPacket[];
  return getGptsFromSqlResult(rows);
}

export async function getLatestRows(
  last_id: number,
  limit: number
): Promise<Gpts[]> {
  const [rows] = await pool.execute(`SELECT * FROM gpts WHERE id > ${last_id} ORDER BY created_at DESC LIMIT ${limit}`) as RowDataPacket[];

  return getGptsFromSqlResult(rows);
}

export async function getRecommendedRows(
  last_id: number,
  limit: number
): Promise<Gpts[]> {
    const [rows] = await pool.execute(`SELECT * FROM gpts WHERE is_recommended=true AND id > ${last_id} ORDER BY sort DESC LIMIT ${limit}`) as RowDataPacket[];
    return getGptsFromSqlResult(rows);
}

export async function getHotRows(
  last_id: number,
  limit: number
): Promise<Gpts[]> {
    const [rows] = await pool.execute(`SELECT * FROM gpts WHERE rating IS NOT null AND id > ${last_id} ORDER BY rating DESC, sort DESC LIMIT ${limit}`) as RowDataPacket[];
    return getGptsFromSqlResult(rows);
}

export async function getTotalCount(): Promise<number> {
  // 使用 MySQL 查询语法
  const [rows] = await pool.execute('SELECT COUNT(*) AS count FROM gpts') as RowDataPacket[];

  // 检查返回的数组是否为空
  if (rows.length === 0) {
    return 0;
  }

  // 获取 count 值
  const row = rows[0];
  return row.count;
}

export async function findByUuid(uuid: string): Promise<Gpts | undefined> {
  // 使用参数化查询
  const [rows] = await pool.execute(`
    SELECT * FROM gpts WHERE uuid = ? LIMIT 1
  `, [uuid]) as RowDataPacket[];

  // 使用 rows.length 来判断行数
  if (rows.length === 0) {
    return undefined;
  }

  // 获取第一行数据
  const row = rows[0];
  const gpts = formatGpts(row);

  return gpts;
}

function getGptsFromSqlResult(rows: RowDataPacket): Gpts[] {
  if (rows.length === 0) {
    return [];
  }

  const gpts: Gpts[] = [];
  rows.forEach((row:any) => {
    const gpt = formatGpts(row);
    if (gpt) {
      gpts.push(gpt);
    }
  });

  return gpts;
}

function formatGpts(row: any): Gpts | undefined {
  // console.log("formatGpts:", row)
  var image = row.avatar_url
  if (image && image != "null") {

  } else {
    image = "/logo.png"
  }

  const gpts: Gpts = {
    uuid: row.uuid,
    org_id: row.org_id,
    name: row.name,
    description: row.description,
    avatar_url: image,//row.avatar_url,
    short_url: row.short_url,
    author_id: row.author_id,
    author_name: row.author_name,
    created_at: row.created_at,
    updated_at: row.updated_at,
    visit_url: row.short_url ? "https://chat.openai.com/g/" + row.short_url : undefined,
    rating: row.rating,
    detail: row.detail, // 直接使用，假设已经是字符串或 undefined
    welcome_message: row.welcome_message
  };

  // try {
  //   gpts.detail = JSON.parse(JSON.stringify(row.detail));
  // } catch (e) {
  //   console.log("parse gpts detail failed: ", e);
  // }

  if (isGptsSensitive(gpts)) {
    return;
  }

  return gpts;
}
