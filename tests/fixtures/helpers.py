from config import Config

def prepare_test_config(cfg):
    """Prepare test server by removing configuration"""
    if cfg.config_exists():
        clean_test_config(cfg)

def clean_test_config(cfg):
    """Clean test server"""
    if cfg.config_exists():
        cfg.config.unlink()
        cfg.path.rmdir()
        cfg.cfg_path.rmdir()
