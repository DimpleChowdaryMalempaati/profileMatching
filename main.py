#!/usr/bin/env python3
"""CLI entry point for the Profile Matching RAG system."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from config import JOB_DESCRIPTIONS_DIR, RESUMES_DIR
from job_matcher import JobMatcher, match_all_jobs
from resume_rag import ResumeRAG, build_index


def cmd_index(args: argparse.Namespace) -> int:
    result = build_index(args.resumes_dir) if args.reset else ResumeRAG().index_resumes(args.resumes_dir)
    print(json.dumps(result, indent=2))
    return 0 if result.get("success") else 1


def cmd_match(args: argparse.Namespace) -> int:
    matcher = JobMatcher()
    if args.all:
        result = match_all_jobs(args.jobs_dir, args.output)
    elif args.text:
        result = matcher.match_job(args.job, top_k=args.top_k)
    else:
        result = matcher.match_job_file(args.job, top_k=args.top_k)

    output = json.dumps(result, indent=2)
    print(output)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    return 0 if result.get("success") else 1


def cmd_stats(args: argparse.Namespace) -> int:
    rag = ResumeRAG()
    print(json.dumps(rag.get_stats(), indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    from tools.resume_loader import list_resumes

    print(json.dumps(list_resumes(args.resumes_dir), indent=2))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    from scripts.generate_dataset import generate_job_descriptions, generate_resumes

    resumes = generate_resumes(args.count)
    jobs = generate_job_descriptions()
    print(json.dumps({
        "success": True,
        "resumes_generated": len(resumes),
        "jobs_generated": len(jobs),
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Profile Matching RAG — index resumes and match jobs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate dataset, build index, match a job
  python main.py generate
  python main.py index --reset
  python main.py match --job job_descriptions/senior_python_ml_engineer.json
  python main.py match --all --output results/all_matches.json

  # List and inspect
  python main.py list
  python main.py stats
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate synthetic resumes and job descriptions")
    p_gen.add_argument("--count", type=int, default=34, help="Number of resumes")
    p_gen.set_defaults(func=cmd_generate)

    p_index = sub.add_parser("index", help="Index resumes into ChromaDB")
    p_index.add_argument("--resumes-dir", default=str(RESUMES_DIR))
    p_index.add_argument("--reset", action="store_true", help="Reset index first")
    p_index.set_defaults(func=cmd_index)

    p_match = sub.add_parser("match", help="Match job description to resumes")
    p_match.add_argument("--job", help="Job file path or inline text with --text")
    p_match.add_argument("--text", action="store_true")
    p_match.add_argument("--all", action="store_true", help="Match all jobs in directory")
    p_match.add_argument("--jobs-dir", default=str(JOB_DESCRIPTIONS_DIR))
    p_match.add_argument("--top-k", type=int, default=10)
    p_match.add_argument("--output")
    p_match.set_defaults(func=cmd_match)

    p_stats = sub.add_parser("stats", help="Show vector index statistics")
    p_stats.set_defaults(func=cmd_stats)

    p_list = sub.add_parser("list", help="List resume files")
    p_list.add_argument("--resumes-dir", default=str(RESUMES_DIR))
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if args.command == "match" and not args.all and not args.job:
        parser.error("--job is required unless --all is used")

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
