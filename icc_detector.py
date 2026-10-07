from androguard.core.apk import APK

apk_path = "sample.apk"

app = APK(apk_path)

manifest = app.get_android_manifest_xml()

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def check_components(tag):

    print(f"\n=== Possible ICC Risks: {tag} ===")

    for component in manifest.iter(tag):

        name = component.get(
            ANDROID_NS + "name"
        )

        exported = component.get(
            ANDROID_NS + "exported"
        )

        permission = component.get(
            ANDROID_NS + "permission"
        )

        if exported == "true" and permission is None:

            print("\nPotential Risk:")
            print("Component:", name)
            print("Reason: Exported without permission")


check_components("activity")
check_components("service")
check_components("receiver")
check_components("provider")