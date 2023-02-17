
import { Translator } from '../../../../translator'
import { Translatable } from '../../../../types/elements'

interface Props {
  dynamicCopy: Translatable // from Python script
  locale: string
}

export const MyComponent = ({ dynamicCopy, locale }: Props): JSX.Element => {
  const dynamicText = Translator.translate(dynamicCopy, locale)

  return (
    <>
      <div>{dynamicText}</div>
    </>
  )
}
