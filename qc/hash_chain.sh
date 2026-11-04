#!/usr/bin/env bash
# 哈希闭链复核：在**发布仓库根目录**运行，把实际执行的命令与原始输出原样落盘。
#
# 为什么用 bash 而不是 Python：复核方手上不一定有本项目环境，但一定有
# git / sha256sum / unzip / stat。这份记录里的每个数字都能被同一条命令复现。
#
# 用法（在发布仓库根目录）：
#   bash qc/hash_chain.sh
# 产出：
#   仓库根目录/独立哈希复核记录.txt
set -u

PKG="delivery-batch20-eval-V3-RELEASE-V3.1"
ZIP="$PKG/part-0001-of-0001.zip"
OUT="独立哈希复核记录.txt"
# 用仓库内的相对路径做解压落点：记录的路径复核方才能照抄，
# 也避免把 Windows 临时目录的绝对路径写进证据（跨机器就失效）。
TMP=".hashcheck_tmp"

# 先打印命令再打印输出 —— 记录里两者都在，读者不必猜这个数字是怎么来的。
run() {
  echo "\$ $*"
  eval "$*"
  echo
}

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

{
  echo "独立哈希复核记录（哈希闭链版）"
  echo "================================================================"
  echo "生成时间（本机）  : $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "生成方式          : 在发布仓库根目录执行 bash qc/hash_chain.sh"
  echo "复核对象          : $ZIP"
  echo ""
  echo "本记录要回答的问题"
  echo "----------------------------------------------------------------"
  echo "上一版 V3.1 在打包过程中被重出过多次，中间某一版的《包校验报告.json》"
  echo "记的是 51f4c6bb…，而最终包是另一个哈希。那是反复修订留下的中间产物，"
  echo "不是数据被改动 —— 但把中间包当证据展示，本身就不该发生。"
  echo ""
  echo "本记录改为：**最终包定稿后**再算一次哈希，并把 ZIP、报告、记录放进"
  echo "同一个提交。下方所有数值均取自定稿后的字节，任何一项不符即视为篡改。"
  echo ""
  echo "一、最终包身份"
  echo "----------------------------------------------------------------"
  run "stat -c %s \"$ZIP\""
  echo "ZIP 文件名 : $(basename "$ZIP")"
  echo ""
  run "sha256sum \"$ZIP\""
  echo ""

  echo "二、解压后成员的 Raw SHA-256（原始字节，不做任何归一）"
  echo "----------------------------------------------------------------"
  echo "\$ unzip -o -q \"$ZIP\" -d $TMP"
  unzip -o -q "$ZIP" -d "$TMP"
  echo ""
  run "sha256sum \"$TMP/facts_audit.json\" \"$TMP/risk_queue.csv\""
  echo "说明一：这里**不做 CRLF→LF 归一**。ZIP 成员按原始字节落盘，"
  echo "        所以复核方用 unzip + sha256sum 拿到的就是上面这两个值。"
  echo "说明二：sha256sum 输出里，哈希与文件名之间有一个模式标记字符（星号 '*' 表示"
  echo "        二进制模式，空格表示文本模式）；它不是哈希的一部分。"
  echo "        哈希本身始终是行首那 64 位十六进制串，跨平台一致。"
  echo ""

  echo "三、与签核文件对账"
  echo "----------------------------------------------------------------"
  echo "$ python - <<'EOF'   # 逐成员算 raw sha256，并与 signoff.final.json::binding 比对"
  python - "$PKG/signoff.final.json" "$TMP" <<'PY'
import hashlib, json, os, sys
fin, tmp = sys.argv[1], sys.argv[2]
b = (json.load(open(fin, encoding="utf-8")) or {}).get("binding") or {}
ok = True
for name, stem in (("facts_audit.json", "facts_audit"),
                   ("risk_queue.csv", "risk_queue")):
    raw = hashlib.sha256(open(os.path.join(tmp, name), "rb").read()).hexdigest()
    want = str(b.get(f"{stem}_sha256_raw") or "")
    same = raw == want
    ok = ok and same
    print(f"{name:<18} 解压实测 {raw}")
    print(f"{'':<18} 签核记录 {want}   -> {'一致' if same else '不一致'}")
    print(f"{'':<18} 结论     {'PASS' if same else 'FAIL'}")
print()
print("总判定：" + ("PASS —— ZIP 内两个成员的原始字节与签核记录逐字节一致"
                 if ok else "FAIL —— 存在不一致，签名与包内容不是同一批产物"))
PY
  echo ""

  echo "四、实际执行的命令清单（可逐条重跑）"
  echo "----------------------------------------------------------------"
  echo "  cd <发布仓库根目录>"
  echo "  stat -c %s $ZIP"
  echo "  sha256sum $ZIP"
  echo "  unzip -o -q $ZIP -d /tmp/x"
  echo "  sha256sum /tmp/x/facts_audit.json /tmp/x/risk_queue.csv"
  echo "  python -c \"import json;print(json.load(open('$PKG/signoff.final.json'))['binding'])\""
  echo ""

  echo "五、关于「最终提交 SHA」—— 为什么本文件里没有它"
  echo "----------------------------------------------------------------"
  echo "git 的提交号 = sha1( tree + parent + author + message )，而 tree 里含"
  echo "本文件的 blob 哈希。让一个文件写出「包含它自身的那个提交」的哈希，等于"
  echo "求解一个固定点：改文件→改 blob→改 tree→改提交号→文件又要改。这不是"
  echo "工程上麻烦，是在数学上不成立。任何声称做到了的，那个值一定是伪造的。"
  echo ""
  echo "所以这一环改由**提交消息**承担（提交消息不参与自身的自指困境）："
  echo "  提交消息  → 声明本文件的 SHA-256 与本 ZIP 的 SHA-256"
  echo "  本文件    → 声明本 ZIP 的 SHA-256 与两个成员的 raw SHA-256"
  echo "  ZIP       → 成员原始字节"
  echo ""
  echo "提交 SHA 由复核方当场用 git 打印（见下一节第 1 条），并与"
  echo "  git ls-tree <提交> -- \"$OUT\""
  echo "给出的 blob 哈希交叉验证：能同时对上，就证明「这份记录确实属于那个提交」，"
  echo "这比文件自己写一个提交号强得多 —— 自写的号码无从证伪。"
  echo ""

  echo "六、复核方验证命令（五条，全部通过即闭链）"
  echo "----------------------------------------------------------------"
  echo "  # 1) 取到提交号与提交消息（消息里应有两个 sha256）"
  echo "  git log -1 --format='%H%n%B'"
  echo ""
  echo "  # 2) 本文件的 blob 哈希必须与 1) 中 git ls-tree 的结果一致"
  echo "  git ls-tree HEAD -- \"$OUT\""
  echo ""
  echo "  # 3) ZIP 的 SHA-256 必须同时等于：本节 1) 消息里的值、"
  echo "  #    本记录第一节的值、《包校验报告.json》的 zip_sha256"
  echo "  sha256sum $ZIP"
  echo "  python -c \"import json;print(json.load(open('$PKG/包校验报告.json'))['zip_sha256'])\""
  echo ""
  echo "  # 4) 两个成员的 raw SHA-256 必须等于本记录第二节的值"
  echo "  unzip -o -q $ZIP -d /tmp/x && sha256sum /tmp/x/facts_audit.json /tmp/x/risk_queue.csv"
  echo ""
  echo "  # 5) 包内自检结果：直接读报告，不需要本项目的源码"
  echo "  python -c \"import json;d=json.load(open('$PKG/包校验报告.json'));print(d['selfcheck']['n_items'],'项 /',d['selfcheck']['n_failed'],'失败 |',d['self_check'])\""
  echo "  # 期望：42 项 / 0 失败 | pass"
  echo ""
  echo "  注：重建自检需主仓库的 qc/bundle_selfcheck.py 与 qc/signoff_v2.py，发布仓库不带源码。"
  echo "  本记录不要求复核方跑它们 —— 结论已在报告里，且第 3、4 条已独立验证了哈希本身。"
  echo ""
  echo "================================================================"
  echo "本记录只陈述可被上述命令复现的事实；不复述任何结论性判断。"
} > "$OUT.raw" 2>&1

# 工具输出（stat / sha256sum / python）在 MSYS 上会带 CRLF，混进来会让本文件
# 变成「CRLF 与 LF 混合」。git 的 text=auto 会在入库时把 CRLF 归一成 LF，
# 于是提交后的字节与本文件自报的哈希对不上 —— 记录自己把自己证伪。
# 所以这里统一成纯 LF：入库归一成为空操作，字节与记录里的哈希恒等。
tr -d '\r' < "$OUT.raw" > "$OUT"
rm -f "$OUT.raw"

echo "已写入 $OUT（$(stat -c %s "$OUT") 字节）"
echo "ZIP SHA-256 : $(sha256sum "$ZIP" | cut -d' ' -f1)"
echo "ZIP 字节数  : $(stat -c %s "$ZIP")"
echo "记录 SHA-256: $(sha256sum "$OUT" | cut -d' ' -f1)"
