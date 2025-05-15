import logging
import json
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from openai import OpenAI



async def main():
    try:
        vulnerabilities = load_sonar_report()
        humor_template = load_humor_template()


        context = await get_mcp_context()
        print("Context:", context)
        context["additional_info"] = PROJECT_CONTEXT_INFO  # 👈 fügt .env-Info ein
        # Generiere den Bericht mit Kontext
        report = await generate_security_report(vulnerabilities, humor_template, context)
        await send_discord_message_async(report)
        logging.info("Full security report sent to Discord")

    except Exception as e:
        logging.error(f"Error in main process: {e}")


if __name__ == "__main__":
    asyncio.run(main())
