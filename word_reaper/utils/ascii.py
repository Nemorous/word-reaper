

from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    print(Fore.RED + Style.BRIGHT + r"""
 __          __           _   _____                             
 \ \        / /          | | |  __ \                            
  \ \  /\  / /__  _ __ __| | | |__) |___  __ _ _ __   ___ _ __  
   \ \/  \/ / _ \| '__/ _` | |  _  // _ \/ _` | '_ \ / _ \ '__| 
    \  /\  / (_) | | | (_| | | | \ \  __/ (_| | |_) |  __/ |    
     \/  \/ \___/|_|  \__,_| |_|  \_\___|\__,_| .__/ \___|_|    
                                              | |                 
                                              |_|        v1.0.1
                                                  By d4rkfl4m3z                
    """)


