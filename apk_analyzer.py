from androguard.core.apk import APK

apk_path = "sample.apk"

app = APK(apk_path)

print("App Name:", app.get_app_name())


manifest = app.get_android_manifest_xml()


def analyze_components(tag):

    print(f"\n=== {tag} ===")

    for component in manifest.iter(tag):

        name = component.get(
            "{http://schemas.android.com/apk/res/android}name"
        )

        exported = component.get(
            "{http://schemas.android.com/apk/res/android}exported"
        )

        permission = component.get(
            "{http://schemas.android.com/apk/res/android}permission"
        )

        print("\nComponent:", name)
        print("Exported:", exported)
        print("Permission:", permission)


analyze_components("activity")
analyze_components("service")
analyze_components("receiver")
analyze_components("provider")