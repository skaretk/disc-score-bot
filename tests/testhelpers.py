
def prepare_test_server(cfg):
    """Prepare test server by removing configuration"""
    if cfg.config_exists():
        cleanup_test_server(cfg)

def cleanup_test_server(cfg):
    """Cleanup test server by removing configuration"""
    cfg.config.unlink()
    cfg.path.rmdir()