import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

console.log("APIキー:", process.env.MOONSHOT_API_KEY ? "読み込まれました" : "読み込めていません");

const client = new OpenAI({
  apiKey: process.env.MOONSHOT_API_KEY,
  baseURL: "https://api.moonshot.ai/v1",
});

async function main() {
  const response = await client.chat.completions.create({
    model: "kimi-k3",
    messages: [
      { role: "user", content: "こんにちは" },
    ],
  });

  console.log(response.choices[0].message.content);
}

main();
