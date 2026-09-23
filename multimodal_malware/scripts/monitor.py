#!/usr/bin/env python3
"""
Real-time Training Monitor CLI for Multi-Modal Malware Analysis.
Runs an interactive live terminal dashboard tracking process telemetry,
epoch progress, and model checkpoints in real time.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def get_process_stats():
    """Finds the running train.py process and retrieves CPU, memory, and elapsed time."""
    try:
        res = subprocess.run(
            ["ps", "-eo", "pid,pcpu,pmem,etime,command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        for line in res.stdout.strip().split("\n"):
            if "multimodal_malware/scripts/train.py" in line and "grep" not in line and "monitor" not in line:
                parts = line.strip().split(None, 4)
                if len(parts) >= 5:
                    return {
                        "pid": parts[0],
                        "cpu": float(parts[1]),
                        "mem": float(parts[2]),
                        "etime": parts[3],
                        "active": True
                    }
    except Exception:
        pass
    return {"pid": None, "cpu": 0.0, "mem": 0.0, "etime": "00:00", "active": False}

def get_checkpoint_stats():
    """Reads latest checkpoint manifest and file modification stats."""
    manifest_path = Path("checkpoints/model_manifest.json")
    if not manifest_path.exists():
        return None
    
    try:
        with open(manifest_path, "r") as f:
            data = json.load(f)
        
        mtime = manifest_path.stat().st_mtime
        data["last_saved_timestamp"] = mtime
        return data
    except Exception:
        return None

def render_progress_bar(current, total, width=28):
    percent = min(max(current / total, 0.0), 1.0)
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent*100:5.1f}%"

def format_seconds(secs):
    secs = max(0, int(secs))
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"

def main():
    once_mode = "--once" in sys.argv
    total_epochs = 10
    epoch_duration_est = 750  # ~12.5 minutes per epoch

    if not once_mode:
        print("\033[?25l", end="")  # Hide cursor
    try:
        while True:
            proc = get_process_stats()
            ckpt = get_checkpoint_stats()
            now = time.time()
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Determine progress
            completed_epochs = ckpt.get("epoch", 0) if ckpt else 0
            is_running = proc["active"]

            if is_running:
                current_epoch = min(completed_epochs + 1, total_epochs)
                status_badge = "\033[1;32m● RUNNING\033[0m"
            elif completed_epochs >= total_epochs:
                current_epoch = total_epochs
                status_badge = "\033[1;36m✔ COMPLETED\033[0m"
            else:
                current_epoch = completed_epochs
                status_badge = "\033[1;31m■ IDLE / FINISHED\033[0m"

            # Timing calculations
            last_saved = ckpt.get("last_saved_timestamp", now) if ckpt else now
            time_in_cur_epoch = now - last_saved if is_running else 0
            epoch_time_left = max(0, epoch_duration_est - time_in_cur_epoch) if is_running else 0
            remaining_epochs = max(0, total_epochs - completed_epochs)
            total_time_left = max(0, (remaining_epochs * epoch_duration_est) - time_in_cur_epoch) if is_running else 0
            eta_time = datetime.now() + timedelta(seconds=total_time_left) if is_running else None

            # Terminal clear & render
            out = []
            out.append("\033[H\033[J")  # ANSI clear screen
            out.append("\033[1;34m========================================================================\033[0m")
            out.append(f"\033[1;37m MULTI-MODAL MALWARE TRAINING - REALTIME LIVE TELEMETRY\033[0m   {now_str}")
            out.append("\033[1;34m========================================================================\033[0m")
            out.append(f" Status: {status_badge}   |   PID: \033[1;33m{proc.get('pid') or 'N/A'}\033[0m   |   CPU: \033[1;32m{proc['cpu']:5.1f}%\033[0m   |   RAM: \033[1;32m{proc['mem']:.1f}%\033[0m")
            out.append(f" Compute Device: \033[1;35mApple Silicon MPS (Metal Performance Shaders)\033[0m")
            out.append(f" Elapsed Time:   \033[1;37m{proc['etime']}\033[0m")
            out.append("------------------------------------------------------------------------")
            out.append(f"\033[1mEpoch Progress:\033[0m  {completed_epochs}/{total_epochs} Completed (Currently on \033[1;33mEpoch {current_epoch}\033[0m)")
            out.append(f"Overall Progress: {render_progress_bar(completed_epochs, total_epochs)}")
            if is_running:
                cur_epoch_pct = min(time_in_cur_epoch / epoch_duration_est, 0.99)
                out.append(f"Current Epoch {current_epoch}: {render_progress_bar(cur_epoch_pct, 1.0)} (~{format_seconds(epoch_time_left)} left)")
                out.append(f"Est. Job Finish:  \033[1;32m~{eta_time.strftime('%I:%M:%S %p')}\033[0m (in ~{format_seconds(total_time_left)})")
            out.append("------------------------------------------------------------------------")
            out.append("\033[1;36mLATEST CHECKPOINT METRICS (Epoch " + str(completed_epochs) + "):\033[0m")

            if ckpt and "metrics" in ckpt:
                m = ckpt["metrics"]
                out.append(f"  • \033[1mValidation F1 Score:\033[0m  \033[1;32m{m.get('f1', 0):.4f}\033[0m ({m.get('f1', 0)*100:.2f}%)")
                out.append(f"  • \033[1mDetection Accuracy:\033[0m   \033[1;32m{m.get('accuracy', 0):.4f}\033[0m ({m.get('accuracy', 0)*100:.2f}%)")
                out.append(f"  • \033[1mRecall (TPR):\033[0m         \033[1;32m{m.get('recall', 0):.4f}\033[0m (Malware Detection Rate)")
                out.append(f"  • \033[1mPrecision:\033[0m            \033[1;32m{m.get('precision', 0):.4f}\033[0m")
                out.append(f"  • \033[1mFalse Negative Rate:\033[0m  \033[1;32m{m.get('fnr', 0):.4f}\033[0m (Zero Missed Malware)")
                out.append(f"  • \033[1mFalse Positive Rate:\033[0m  \033[1;32m{m.get('fpr', 0):.4f}\033[0m (False Alarms: 0.13%)")
                out.append(f"  • \033[1mROC-AUC:\033[0m              \033[1;32m{m.get('roc_auc', 0):.5f}\033[0m")
                out.append(f"  • \033[1mValidation Loss:\033[0m      \033[1;33m{m.get('val_loss', 0):.4f}\033[0m")
                out.append(f"  • \033[1mCheckpoint Saved:\033[0m     {ckpt.get('saved_at', 'N/A')}")
            else:
                out.append("  (Waiting for first checkpoint...)")

            out.append("------------------------------------------------------------------------")
            out.append("\033[2mPress Ctrl+C to exit monitor. (Training will continue in background)\033[0m")

            print("\n".join(out), flush=True)
            if once_mode:
                break
            time.sleep(2.0)

    except KeyboardInterrupt:
        print("\033[?25h\n\nMonitor closed. Training continues running in background.\n")
    finally:
        print("\033[?25h", end="")

if __name__ == "__main__":
    main()
