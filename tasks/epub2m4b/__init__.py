import tempfile

from pathlib import Path
from epub2speech import convert_epub_to_m4b, AzureTextToSpeech
from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
  epub: str
  m4b: str | None
  voice: str
  key: str
  region: typing.Literal["eastasia", "southeastasia", "australiaeast", "northeurope", "westeurope", "eastus", "eastus2", "southcentralus", "westcentralus", "westus", "westus2", "brazilsouth"]
  max_chapters: int | None
class Outputs(typing.TypedDict):
  m4b: str
#endregion

def main(params: Inputs, context: Context) -> Outputs:
  temp_dir = tempfile.TemporaryDirectory()
  output_path = params["m4b"]
  if output_path is None:
    output_path = Path(context.session_dir) / f"{context.job_id}.m4b"
  try:
    output_path = convert_epub_to_m4b(
      epub_path=Path(params["epub"]),
      workspace=Path(temp_dir.name),
      output_path=Path(output_path),
      voice=params["voice"],
      max_chapters=params["max_chapters"],
      progress_callback=lambda e: context.report_progress(e.progress),
      tts_protocol=AzureTextToSpeech(
        subscription_key=params["key"],
        region=params["region"],
      ),
    )
    if output_path is None:
      raise ValueError("Cannot find content to generate")
    return { "m4b": str(output_path) }

  finally:
    temp_dir.cleanup()