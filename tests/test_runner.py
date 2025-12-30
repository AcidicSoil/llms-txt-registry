import subprocess
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.generator_runner.runner import GeneratorRunner
from src.registry_config.models import Source

@patch("subprocess.run")
def test_runner_success(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    # Mock successful result
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Success"
    mock_run.return_value = mock_result
    
    # Create fake artifact
    (tmp_path / "temp_work" / "test-src").mkdir(parents=True)
    (tmp_path / "temp_work" / "test-src" / "test-llms.txt").touch()
    
    result = runner.run_source(source)
    
    assert result["status"] == "success"
    assert "test-llms.txt" in result["artifacts"][0]
    
    # Verify command structure - UPDATED to check for 'lmstxt'
    args, kwargs = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "lmstxt"
    assert cmd[1] == "https://github.com/test/repo"
    assert "--output-dir" in cmd
    assert "--stamp" in cmd

@patch("subprocess.run")
def test_runner_failure(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Error"
    mock_run.return_value = mock_result
    
    result = runner.run_source(source)
    assert result["status"] == "failure"
    assert result["error"] == "Error"

@patch("subprocess.run")
def test_runner_timeout(mock_run, tmp_path):
    runner = GeneratorRunner(output_root=tmp_path)
    source = Source(id="test-src", url="https://github.com/test/repo")
    
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=300)
    
    result = runner.run_source(source)
    assert result["status"] == "failure"
    assert "timed out" in result["error"]