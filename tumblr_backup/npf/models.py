from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag, TypeAdapter
from typing import Annotated, Any, ClassVar, Literal

__all__ = [
    'AppAttribution',
    'AskLayout',
    'Attribution',
    'AudioBlock',
    'BlogAttribution',
    'BlogInfo',
    'CarouselMode',
    'ContentBlock',
    'IFrame',
    'ImageBlock',
    'InlineFormat',
    'InlineFormatBasic',
    'InlineFormatColor',
    'InlineFormatLink',
    'InlineFormatMention',
    'Layout',
    'LinkAttribution',
    'LinkBlock',
    'Media',
    'Options',
    'PaywallBlock',
    'PaywallBlockCta',
    'PaywallBlockDivider',
    'PollAnswer',
    'PollBlock',
    'PollSettings',
    'Post',
    'PostAttribution',
    'RendererOptions',
    'RowsDisplay',
    'RowsLayout',
    'TextBlock',
    'TextBlockIndented',
    'TextBlockNoIndent',
    'VideoBlock',
    'VisualMedia',
]


class Media(BaseModel):
    """
    An NPF media object.

    See: https://www.tumblr.com/docs/npf#media-objects
    """

    """The canonical URL of the media asset."""
    url: str

    """
    The MIME type of the media asset, or a best approximation will be made
    based on the given URL.
    """
    type: str | None = None


class VisualMedia(Media):
    """An image or video media object."""

    """
    The width of the media asset, if that makes sense (for images and videos,
    but not for audio).
    """
    width: int

    """
    The height of the media asset, if that makes sense (for images and videos,
    but not for audio).
    """
    height: int

    """For display purposes, this indicates whether the dimensions are defaults."""
    original_dimensions_missing: bool | None = None

    """
    This indicates whether this media object is a cropped version of the
    original media.
    """
    cropped: bool | None = None

    """
    This indicates whether this media object has the same dimensions as the
    original media
    """
    has_original_dimensions: bool | None = None


class BlogInfo(BaseModel):
    """Information about a particular blog on Tumblr."""

    """The blog's UUID."""
    uuid: str

    """The blog's username."""
    name: str

    """The blog's URL."""
    url: str


class Post(BaseModel):
    """A reference to a Tumblr post."""

    id: str


class PostAttribution(BaseModel):
    """
    Attributes an image to a particular post.

    See: https://www.tumblr.com/docs/npf#attribution-type-post
    """

    type: Literal['post']

    """The URL of the post to be attributed."""
    url: str

    """The post to be attributed."""
    post: Post

    """The blog whose post is attributed."""
    blog: BlogInfo


class LinkAttribution(BaseModel):
    """
    Attributes an image to an arbitrary link.

    See: https://www.tumblr.com/docs/npf#attribution-type-link
    """

    type: Literal['link']

    """The URL to be attributed for the content."""
    url: str


class BlogAttribution(BaseModel):
    """
    Attributes something to a specific Tumblr blog.

    See: https://www.tumblr.com/docs/npf#attribution-type-blog
    """

    type: Literal['blog']

    """The blog to which this is attributed."""
    blog: BlogInfo


class AppAttribution(BaseModel):
    """
    Attributes something to a third-party app.

    See: https://www.tumblr.com/docs/npf#attribution-type-app
    """

    type: Literal['app']

    """The canonical URL to the source content in the third-party app."""
    url: str

    """The name of the application to be attributed."""
    app_name: str | None = None

    """Any display text that the client should use with the attribution."""
    display_text: str | None = None

    """
    A specific logo that the client should use with the third-party app
    attribution.
    """
    logo: VisualMedia | None = None


"""Attribution indicating where a content or layout block came from."""
Attribution = Annotated[
    PostAttribution | LinkAttribution | BlogAttribution | AppAttribution, Field(discriminator='type')
]


class CarouselMode(BaseModel):
    """The carousel display mode."""

    type: Literal['carousel']


class RowsDisplay(BaseModel):
    """
    An object describing how to display a single row.

    See: https://www.tumblr.com/docs/npf#layout-block-display-mode-carousel
    """

    """An array of block indices to use in this row."""
    blocks: list[int]

    """The display mode for this row."""
    mode: CarouselMode | None = None


class RowsLayout(BaseModel):
    """
    Content blocks organized in rows, with variable elements per row.

    See: https://www.tumblr.com/docs/npf#layout-block-type-rows
    """

    type: Literal['rows']

    """A list of ways to display sets of rows."""
    display: list[RowsDisplay]

    """How the content should be truncated."""
    truncate_after: int | None = None


class AskLayout(BaseModel):
    """
    Content blocks that are part of an ask.

    See: https://www.tumblr.com/docs/npf#layout-block-type-ask
    """

    type: Literal['ask']

    """An array of block indices that are a part of the ask content of the Post."""
    blocks: list[int]

    """
    If the ask is not anonymous, this will include information about the blog
    that submitted the ask.
    """
    attribution: BlogAttribution | None = None


"""
A layout indicating how to lay out contents blocks.

See: https://www.tumblr.com/docs/npf#layout-blocks
"""
Layout = Annotated[AskLayout | RowsLayout, Field(discriminator='type')]


class InlineFormatBasic(BaseModel):
    """
    Basic inline formatting types that require no additional information.

    See: https://www.tumblr.com/docs/npf#inline-format-types-bold-italic-strikethrough-small
    """

    type: Literal['bold', 'italic', 'strikethrough', 'small']

    """The starting index of the formatting range (inclusive)."""
    start: int

    """The ending index of the formatting range (inclusive)."""
    end: int


class InlineFormatLink(BaseModel):
    """
    An inline link.

    See: https://www.tumblr.com/docs/npf#inline-format-type-link
    """

    type: Literal['link']

    """The starting index of the formatting range (inclusive)."""
    start: int

    """The ending index of the formatting range (inclusive)."""
    end: int

    """The link's URL."""
    url: str


class InlineFormatMention(BaseModel):
    """
    A mention of another blog.

    See: https://www.tumblr.com/docs/npf#inline-format-type-mention
    """

    type: Literal['mention']

    """The starting index of the formatting range (inclusive)."""
    start: int

    """The ending index of the formatting range (inclusive)."""
    end: int

    """The mentioned blog."""
    blog: BlogInfo


class InlineFormatColor(BaseModel):
    """
    Colored text.

    See: https://www.tumblr.com/docs/npf#inline-format-type-color
    """

    type: Literal['color']

    """The starting index of the formatting range (inclusive)."""
    start: int

    """The ending index of the formatting range (inclusive)."""
    end: int

    """The color to use, in standard hex format, with leading #."""
    hex: str


"""
A single piece of inline formatting for a TextBlock.

See: https://www.tumblr.com/docs/npf#inline-formatting-within-a-text-block
"""
InlineFormat = Annotated[
    InlineFormatBasic | InlineFormatLink | InlineFormatMention | InlineFormatColor,
    Field(discriminator='type'),
]


class TextBlockBase(BaseModel):
    """
    The base interface for all types of text blocks.
    """

    type: Literal['text']

    """The text to use inside this block."""
    text: str

    """
    The subtype of text block.

    See: https://www.tumblr.com/docs/npf#text-block-subtypes
    """
    subtype: Literal[
        'heading1', 'heading2', 'quirky', 'quote', 'chat', 'indented', 'ordered-list-item', 'unordered-list-item'
    ] | None = None

    """
    Inline formatting for this text.

    See: https://www.tumblr.com/docs/npf#inline-formatting-within-a-text-block
    """
    formatting: list[InlineFormat] | None = None


class TextBlockNoIndent(TextBlockBase):
    """
    A text block of a type that doesn't allow indentation.

    See: https://www.tumblr.com/docs/npf#content-block-type-text
    """

    subtype: Literal['heading1', 'heading2', 'quirky', 'quote', 'chat'] | None = None


class TextBlockIndented(TextBlockBase):
    """
    A text block of a type that allows indentation.

    See: https://www.tumblr.com/docs/npf#content-block-type-text
    """

    """
    The subtype of text block.

    See: https://www.tumblr.com/docs/npf#text-block-subtypes
    """
    subtype: Literal['indented', 'ordered-list-item', 'unordered-list-item']

    """See: https://www.tumblr.com/docs/npf#text-block-subtype-list-item"""
    indent_level: int | None = None


def textblock_discriminator(v: Any) -> str:
    if isinstance(v, dict):
        st = v.get('subtype')
    else:
        # model instance during serialization
        st = getattr(v, 'subtype', None)

    if st in {'indented', 'ordered-list-item', 'unordered-list-item'}:
        return 'indented'

    return 'noindent'


"""An NPF text type content block."""
TextBlock = Annotated[
    Annotated[TextBlockNoIndent, Tag('noindent')] | Annotated[TextBlockIndented, Tag('indented')],
    Discriminator(textblock_discriminator),
]


class ImageBlock(BaseModel):
    """
    An NPF image type content block.

    See: https://www.tumblr.com/docs/npf#content-block-type-image
    """

    type: Literal['image']

    """
    An array of VisualMedia objects which represent different available
    sizes of this image asset.
    """
    media: list[VisualMedia]

    """Colors used in the image."""
    colors: dict[str, str] | None = None

    """A feedback token to use when this image block is a GIF Search result."""
    feedback_token: str | None = None

    """
    For GIFs, this is a single-frame "poster".

    See: https://www.tumblr.com/docs/npf#gif-posters
    """
    poster: VisualMedia | None = None

    """See: https://www.tumblr.com/docs/npf#attributions"""
    attribution: Attribution | None = None

    """Text used to describe the image, for screen readers."""
    alt_text: str | None = None

    """A caption typically shown under the image."""
    caption: str | None = None


class AudioBlock(BaseModel):
    """
    An NPF audio type content block.

    See: https://www.tumblr.com/docs/npf#content-block-type-audio
    """

    type: Literal['audio']

    """
    The URL to use for the audio block. Either this, media, or both
    will always be set.
    """
    url: str | None = None

    """
    The Media to use for the audio block. Either this, url, or
    both will always be set.
    """
    media: Media | None = None

    """
    The provider of the audio source, whether it's tumblr for native audio or
    a trusted third party.
    """
    provider: str | None = None

    """The title of the audio asset."""
    title: str | None = None

    """The artist of the audio asset."""
    artist: str | None = None

    """The album from which the audio asset originated."""
    album: str | None = None

    """
    An image media object to use as a "poster" for the audio track, usually
    album art.
    """
    poster: list[VisualMedia] | None = None

    """HTML code that could be used to embed this audio track into a webpage."""
    embed_html: str | None = None

    """A URL to the embeddable content to use as an iframe."""
    embed_url: 'str | None' = None

    """Optional provider-specific metadata about the audio track."""
    metadata: dict[str, object] | None = None

    """Optional attribution information about where the audio track came from."""
    attribution: Attribution | None = None


class LinkBlock(BaseModel):
    """
    An NPF link type content block.

    See: https://www.tumblr.com/docs/npf#content-block-type-link
    """

    type: Literal['link']

    """The URL to use for the link block."""
    url: str

    """The title of where the link goes."""
    title: str | None = None

    """The description of where the link goes."""
    description: str | None = None

    """The author of the link's content."""
    author: str | None = None

    """The name of the site being linked to."""
    site_name: str | None = None

    display_url: str | None = None

    """An image media object to use as a "poster" for the link."""
    poster: list[VisualMedia] | None = None


class IFrame(BaseModel):
    """
    An NPF iframe object.

    See: https://www.tumblr.com/docs/npf#embed-iframe-objects
    """

    """A URL used for constructing and embeddable video iframe."""
    url: str

    """The width of the video iframe"""
    width: int

    """The height of the video iframe"""
    height: int


class VideoBlock(BaseModel):
    """
    An NPF video type content block.

    See: https://www.tumblr.com/docs/npf#content-block-type-video
    """

    type: Literal['video']

    """
    The URL to use for the video block. Either this, media, or both
    will always be set.
    """
    url: str | None = None

    """
    The Media to use for the video block. Either this, url, or
    both will always be set.
    """
    media: VisualMedia | None = None

    """
    The provider of the audio source, whether it's tumblr for native audio or
    a trusted third party.
    """
    provider: str | None = None

    """HTML code that could be used to embed this video into a webpage."""
    embed_html: str | None = None

    """An IFrame used for constructing video iframes."""
    embed_iframe: IFrame | None = None

    """A URL to the embeddable content to use as an iframe."""
    embed_url: 'str | None' = None

    """
    An image media object to use as a "poster" for the video, usually a single
    frame.
    """
    poster: list[VisualMedia] | None = None

    """Optional provider-specific metadata about the video."""
    metadata: dict[str, object] | None = None

    """Optional attribution information about where the video came from."""
    attribution: Attribution | None = None

    """Whether this video can be played on a cellular connection."""
    can_autoplay_on_cellular: bool | None = None

    """The video duration in milliseconds."""
    duration: int | None = None


class PollAnswer(BaseModel):
    """One possible answer to a poll."""

    """The UUID for this answer."""
    client_id: str

    """The text describing this answer."""
    answer_text: str


class PollSettings(BaseModel):
    """The settings used to create this poll."""

    """Whether the poll allows multiple choices."""
    multiple_choice: bool

    """
    Meaning unclear.

    This seems to be "closed-after" whether the poll is open or closed.
    """
    close_status: str

    """The number of seconds after the poll's creation that it expires."""
    expire_after: int

    """The name of the app that created the poll. Usually "tumblr"."""
    source: str


class PollBlock(BaseModel):
    """
    An NPF poll type content block.

    This is not an officially-documented block type, so its documentation is
    best-effort.
    """

    type: Literal['poll']

    """The UUID for this poll."""
    client_id: str

    """The question this poll is answering."""
    question: str

    """The possible answers for the poll."""
    answers: list[PollAnswer]

    """The settings for creating this poll."""
    settings: PollSettings

    """A string representation of the moment this poll was created."""
    created_at: str

    """
    The number of *seconds* (not milliseconds) since the epoch at which this
    poll was created.
    """
    timestamp: int


class PaywallBlockCta(BaseModel):
    """
    A CTA (unpaid) or disabled paywall block.

    See: https://www.tumblr.com/docs/npf#content-block-type-paywall
    """

    type: Literal['paywall']

    """The paywall block design."""
    subtype: Literal['cta', 'disabled']

    """The creator profile url this paywall should link to."""
    url: str

    """Whether this paywall block is actually visible, default to true."""
    is_visible: bool | None = None

    """The CTA title that appears above the main text."""
    title: str

    """The main description text."""
    text: str


class PaywallBlockDivider(BaseModel):
    """
    A paywall block that appears as a divider.

    See: https://www.tumblr.com/docs/npf#content-block-type-paywall
    """

    type: Literal['paywall']

    """The paywall block design."""
    subtype: Literal['divider']

    """The creator profile url this paywall should link to."""
    url: str

    """Whether this paywall block is actually visible, default to true."""
    is_visible: bool | None = None

    """The label text."""
    text: str

    """The hex color for the label and divider, e.g. #eeeeee."""
    color: str | None = None


"""An NPF paywall type content block."""
PaywallBlock = Annotated[
    PaywallBlockCta | PaywallBlockDivider, Field(discriminator='subtype')
]


"""
A single discrete unit of content.

See: https://www.tumblr.com/docs/npf#content-blocks
"""
ContentBlock = Annotated[
    AudioBlock | ImageBlock | LinkBlock | PaywallBlock | PollBlock | TextBlock | VideoBlock,
    Field(discriminator='type'),
]

ContentBlockList = list[ContentBlock]

_content_block_list_adapter = TypeAdapter(ContentBlockList)


class RendererOptions(BaseModel):
    """A custom Renderer configuration to use to convert NPF components to HTML."""

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

    prefix: str | None = None
    asking_avatar: list[VisualMedia] | None = Field(None, alias='askingAvatar')


class Options(BaseModel):
    """Options for npf2html rendering."""

    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

    """
    The prefix to use for class names used to disambiguate block types and
    subtypes that don't map cleanly to HTML tags. Defaults to "npf".

    This is also used for CSS variables to convey additional style information
    about the blocks.
    """
    prefix: str | None = None

    """
    The layouts describing how to group different content blocks.

    This is available from `post.layout` in the Tumblr API.
    """
    layout: list[Layout] | None = None

    """
    The VisualMedia to use for the asker's avatar if the post being
    rendered is an ask.

    This is available from `post.asking_avatar` in the Tumblr API.
    """
    asking_avatar: 'list[VisualMedia] | None' = Field(default=None, alias='askingAvatar')

    """
    A custom Renderer to use to convert NPF components to HTML.

    If this is passed, prefix and asking_avatar are ignored in
    favor of the corresponding values in the renderer.
    """
    renderer: RendererOptions | None = None
