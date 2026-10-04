---
name: sync-upstream
description: Sync this QQMusicApi fork with the upstream L-1124 main branch while preserving local customizations and validating the merged result.
---

# Sync Upstream

同步 `/Users/nichuanfang/workspace/python/QQMusicApi` 的上游 `L-1124/QQMusicApi`，保留本 fork 的生产定制，并在合并后完成完整验证。

## 前置边界

* 只有用户明确要求时才执行 `git push`；默认只创建本地 merge commit。
* 合并前先检查工作区。未提交的 `web/Dockerfile` 定制是本 fork 的持久变更，不要把它并入同步提交。
* `.DS_Store` 不入库。

## 操作流程

1. 读取 `docs/contributing.md`，确认当前分支与 `origin`、`upstream` 状态。
2. 确认 `upstream` 是 `https://github.com/L-1124/QQMusicApi.git`，然后执行 `git fetch upstream --prune`。
3. 用 `git rev-list --left-right --count HEAD...upstream/main` 判断落后情况；若无需更新则停止。
4. 用 `git merge upstream/main --no-commit --no-ff` 开始合并。不要使用 rebase 或 squash，保留 fork 与上游的真实合并历史。
5. 冲突时优先查看两侧提交语义，不要机械选边。
   * 本地 `web/Dockerfile` 定制继续保留在未提交工作区。
   * 旧版 `web/src/adapter/lyric_decrypt_adapter.py` 已失效：它依赖被移除的 `RouteContext.client`。新版 `GetLyricResponse` 的 model validator 会内置 QRC 解密，应采用上游 lyric route 并删除该 adapter。
6. 把合并结果加入暂存区，但显式还原 `web/Dockerfile` 的未提交定制，再创建中文 Conventional/Gitmoji merge commit。历史同类型提交使用 `🔀 chore(sync): 同步上游最新代码`。
7. 按仓库规约验证，至少执行：

   ```bash
   uv sync --all-groups
   uv run ruff check qqmusic_api tests
   uv run pyrefly check
   uv run pytest
   uv run pytest web/tests
   uv run prek run --all-files
   uv run zensical build
   ```

   上游新增 Web 依赖分组后，普通 `uv sync` 不会安装 `fastapi`/`uvicorn` 等包，必须用 `--all-groups`。
8. 若 `prek` 自动修复文件，把修复纳入同步提交；不处理无关的 `.DS_Store`。
9. 汇报同步前后 ahead/behind、merge commit、冲突决策、跳过的真实网络测试原因、检查结果，并确认是否需要推送。

## 适配评估

同步后如用户关心下游集成（例如 GYMDL），只核对实际调用的 Web path、参数和响应字段。当前 GYMDL 兼容处理：

* `QQSongDetail`: `track` / `track_info`
* `QQURL`: `data` / `midurlinfo`
* `QQPlaylist`: `songs` / `songlist`
* 封面不走 `/album/get_cover`，直接用歌曲数据里的 `pmid` 拼 `y.gtimg.cn/music/photo_new/T002R300x300M000{pmid}.jpg`
