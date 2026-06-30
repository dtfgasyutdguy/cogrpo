import mesop.labs as mel


@mel.web_component(path="./web_component.js")

  return mel.insert_web_component(
# def web_component(array: list[str], object: dict[str, str]):
    name="complex-prop-component",
    properties={
      "array": array,
      "object": object,
    },
  )
