import { Weak } from '../../../../helpers'
import { PropsUIPageEnd } from '../../../../types/pages'
import { ReactFactoryContext } from '../../factory'
import { Footer } from './templates/footer'
import { Sidebar } from './templates/sidebar'
import LogoSvg from '../../../../../assets/images/logo.svg'
import { Page } from './templates/page'
import TextBundle from '../../../../text_bundle'
import { Translator } from '../../../../translator'
import { BodyLarge, Title1 } from '../elements/text'

type Props = Weak<PropsUIPageEnd> & ReactFactoryContext

export const EndPage = (props: Props): JSX.Element => {
  const { title, text, text1 } = prepareCopy(props)

  const footer: JSX.Element = <Footer />

  const sidebar: JSX.Element = <Sidebar logo={LogoSvg} />

  const body: JSX.Element = (
    <>
      <Title1 text={title} />
      <BodyLarge text={text} />
      <BodyLarge text={text1} />
    </>
  )

  return (
    <Page
      body={body}
      sidebar={sidebar}
      footer={footer}
    />
  )
}

interface Copy {
  title: string
  text: string
  text1: string
}

function prepareCopy ({ locale }: Props): Copy {
  return {
    title: Translator.translate(title, locale),
    text: Translator.translate(text, locale),
    text1: Translator.translate(text1, locale)
  }
}

const title = new TextBundle()
  .add('en', 'Thank you')
  .add('nl', 'Bedankt')

function generateRandomString (length: number, num: number): string {
  let result = ''
  const numberChars = '0123456789'
  const letterChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  const characters = num === 1 ? numberChars : letterChars
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length))
  }
  return result
}
// Generate a random string of 5 numbers and 5 letters
const numbers: string = generateRandomString(5, 1)
const letters: string = generateRandomString(5, 2)

// Combine the 'abcde' prefix with the random numbers and letters
const randomStringen: string = `Your return code is don0223${numbers}${letters}`
const randomStringnl: string = `Uw retourcode is don0223${numbers}${letters} `

const text = new TextBundle()
  .add('en', randomStringen)
  .add('nl', randomStringnl)

const text1 = new TextBundle()
  .add('en', '\nPlease copy and paste your return code to the survey page. After you finish this, you can close this page.')
  .add('nl', '\nGelieve uw terugkeercode te kopiëren en te plakken op de enquêtepagina. Nadat u dit hebt voltooid, kunt u deze pagina sluiten.')
