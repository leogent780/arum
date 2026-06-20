#!/usr/bin/env python3
"""
TikTok 계정 영상 다운로더
- accounts.txt에 TikTok 계정 URL을 한 줄씩 입력
- 각 계정에서 최신순으로 최대 100개 영상 다운로드
"""

import subprocess
import sys
import os
from pathlib import Path


ACCOUNTS_FILE = "accounts.txt"
OUTPUT_DIR = "downloads"
MAX_VIDEOS = 100


def check_yt_dlp():
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        print(f"yt-dlp 버전: {result.stdout.strip()}")
    except FileNotFoundError:
        print("yt-dlp가 설치되어 있지 않습니다. 설치 중...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
        print("yt-dlp 설치 완료!")


def load_accounts():
    if not Path(ACCOUNTS_FILE).exists():
        # 예시 파일 생성
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            f.write("# TikTok 계정 URL을 한 줄씩 입력하세요 (# 으로 시작하는 줄은 무시됩니다)\n")
            f.write("# 예시:\n")
            f.write("# https://www.tiktok.com/@username1\n")
            f.write("# https://www.tiktok.com/@username2\n")
        print(f"'{ACCOUNTS_FILE}' 파일이 생성되었습니다.")
        print("파일을 열어서 다운로드할 TikTok 계정 URL을 입력하고 다시 실행하세요.")
        sys.exit(0)

    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    accounts = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            accounts.append(line)

    return accounts


def download_account(account_url: str, output_dir: str):
    username = account_url.rstrip("/").split("/")[-1].lstrip("@")
    save_path = os.path.join(output_dir, username)
    os.makedirs(save_path, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"계정: {account_url}")
    print(f"저장 경로: {save_path}")
    print(f"최대 다운로드: {MAX_VIDEOS}개")
    print(f"{'='*60}")

    cmd = [
        "yt-dlp",
        "--playlist-end", str(MAX_VIDEOS),   # 최신순 100개
        "--output", os.path.join(save_path, "%(upload_date)s_%(id)s.%(ext)s"),
        "--format", "best",
        "--no-warnings",
        "--ignore-errors",                    # 개별 영상 오류 시 건너뜀
        "--sleep-interval", "1",              # 요청 간 1초 대기 (차단 방지)
        "--max-sleep-interval", "3",
        "--retries", "3",
        account_url,
    ]

    try:
        result = subprocess.run(cmd, text=True)
        if result.returncode == 0:
            print(f"\n[완료] {username} 다운로드 성공!")
        else:
            print(f"\n[경고] {username} 일부 영상 다운로드 실패 (오류 코드: {result.returncode})")
    except KeyboardInterrupt:
        print("\n사용자가 다운로드를 중단했습니다.")
        sys.exit(0)


def main():
    print("=" * 60)
    print("  TikTok 영상 다운로더 (개인 사용 목적)")
    print("=" * 60)

    check_yt_dlp()

    accounts = load_accounts()

    if not accounts:
        print(f"'{ACCOUNTS_FILE}' 파일에 계정 URL이 없습니다.")
        print("파일을 열어서 TikTok 계정 URL을 입력하세요.")
        sys.exit(0)

    print(f"\n총 {len(accounts)}개 계정 발견:")
    for i, acc in enumerate(accounts, 1):
        print(f"  {i}. {acc}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, account_url in enumerate(accounts, 1):
        print(f"\n[{i}/{len(accounts)}] 처리 중...")
        download_account(account_url, OUTPUT_DIR)

    print(f"\n{'='*60}")
    print(f"모든 다운로드 완료! 저장 위치: ./{OUTPUT_DIR}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
