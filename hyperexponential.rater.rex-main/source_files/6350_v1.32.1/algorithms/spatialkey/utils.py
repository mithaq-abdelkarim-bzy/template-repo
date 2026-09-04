class UploadSpatialKeyProgress:
    def __init__(self, hxd, progress, num_stages, num_rows=None, num_dfs=None):
        """
        Parameters
        ----------
        hxd : model hxd object
        progress : model progress object
        num_stages : int
            The number of stages each dataframe goes through during processing.
            ie. the number of update() calls in the for loop
        num_dfs : int
            The number of dataframes we are processing. If not provided at initialization, 
            the progress will show a "Preparing upload..." message until set via 
            `set_num_dfs()`.
        """
        self.hxd = hxd
        self.progress = progress
        self.num_stages = num_stages
        self.num_rows = num_rows
        self.num_dfs = num_dfs
        self.total = None
        self.current_stage = 0
        self.percent = 0

        if self.num_dfs is not None:
            self._recalculate_total()
        else:
            # placeholder status until num_dfs is known
            self.hxd.spatialkey.fetch_status = "⏳ Preparing upload..."

    def _recalculate_total(self):
        # example: 7 update() calls in the loop * number of times we loop + 2 update() call outside of the loop
        self.total = self.num_stages * self.num_dfs + 1

    def set_num_dfs(self, num_dfs):
        self.num_dfs = num_dfs
        self._recalculate_total()

    def set_num_rows(self, num_rows):
        self.num_rows = num_rows

    def _get_label(self):
        if self.total:
            self.percent = int(self.current_stage / self.total * 100)
            return f"⏳ Uploading..... {self.percent}%"
        else:
            return "⏳ Preparing upload..."

    def update(self):
        self.hxd.spatialkey.fetch_status = self._get_label()
        self.progress.update(self.percent / 100 if self.total else 0)
        self.current_stage += 1

    def finish(self):
        self.hxd.spatialkey.fetch_status = f"✅ Applied SpatialKey to {self.num_rows} data points in schedule table"

    def skip(self):
        self.current_stage += self.num_stages
