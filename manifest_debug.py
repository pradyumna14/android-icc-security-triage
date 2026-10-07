from androguard.core.apk import APK
from lxml import etree

app = APK("sample.apk")

manifest = app.get_android_manifest_xml()

print(etree.tostring(
    manifest,
    pretty_print=True,
    encoding="unicode"
))