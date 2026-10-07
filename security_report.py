from androguard.core.apk import APK
import json

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

app = APK("sample.apk")
manifest = app.get_android_manifest_xml()

report = {
    "application": app.get_app_name(),
    "icc_findings": []
}

for activity in manifest.iter("activity"):

    name = activity.get(ANDROID_NS + "name")
    exported = activity.get(ANDROID_NS + "exported")
    permission = activity.get(ANDROID_NS + "permission")

    if exported != "true":
        continue

    actions = []
    categories = []

    for intent_filter in activity.findall("intent-filter"):

        for action in intent_filter.findall("action"):
            action_name = action.get(ANDROID_NS + "name")
            if action_name:
                actions.append(action_name)

        for category in intent_filter.findall("category"):
            category_name = category.get(ANDROID_NS + "name")
            if category_name:
                categories.append(category_name)

    report["icc_findings"].append({
        "type": "activity",
        "component": name,
        "exported": True,
        "permission": permission,
        "actions": list(set(actions)),
        "categories": list(set(categories))
    })

with open("security_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("security_report.json created!")