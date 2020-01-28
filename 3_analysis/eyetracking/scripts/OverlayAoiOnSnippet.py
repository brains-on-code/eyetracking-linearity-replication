import json
from os import path

from PIL import Image, ImageDraw, ImageFont

import config


def compute_aois(resolution, snippet, scrambled=False):
    base_resolution = resolution

    if scrambled:
        base_resolution += '_scrambled'

    with open(path.join("studies", config.CURRENT_STUDY, "images/aoi", snippet + ".json")) as json_file:
        aoi_data = json.load(json_file)
        base_x = aoi_data[base_resolution]['base_x']
        base_y = aoi_data[base_resolution]['base_y']
        base_indent_x = aoi_data[base_resolution]['base_indent_x']
        base_indent_y = aoi_data[base_resolution]['base_indent_y']

        story_order = aoi_data['story_order']
        execution_order = aoi_data['execution_order']

        AOIs = {
            "base_x": base_x,
            "base_y": base_y,
            "base_indent_x": base_indent_x,
            "base_indent_y": base_indent_y,
            "lines": [],
            "blocks": [],
            "answer": {}
        }

        for line_nr, line in enumerate(aoi_data['lines']):
            # skip empty lines
            if not line:
                continue

            if 'start_x' in line:
                start_x = line['start_x']
            else:
                start_x = (base_x + (base_indent_x * line['indent_x']))

            start_y = base_y + (base_indent_y * line_nr)

            if 'width' in line:
                end_x = start_x + line['width']
            else:
                end_x = line[resolution + '_end_x']

            end_y = start_y + base_indent_y

            AOIs['lines'].append({
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y
            })

        for block_nr, block in enumerate(aoi_data['blocks']):
            start_x = base_x + (base_indent_x * block['indent_x'])
            start_y = base_y + (base_indent_y * block['start'])

            end_x = block[resolution + '_end_x']
            end_y = (start_y + block['lines'] * base_indent_y)

            AOIs['blocks'].append({
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y
            })

        if resolution == '1050':
            AOIs['answer'] = {
                "start_x": 385,
                "start_y": 950,
                "end_x": 1310,
                "end_y": 1050
            }
        elif resolution == '1080':
            AOIs['answer'] = {
                "start_x": 495,
                "start_y": 975,
                "end_x": 1435,
                "end_y": 1080
            }
        else:
            AOIs['answer'] = {
                "start_x": 460,
                "start_y": 1100,
                "end_x": 1460,
                "end_y": 1200
            }

    return [AOIs, story_order, execution_order]


def draw_snippet_aoi_overlay(resolution, snippet, scrambled=False):
    image_path = path.join("studies", config.CURRENT_STUDY, "images", resolution, snippet)
    base_resolution = resolution

    if scrambled:
        image_path += '_scrambled'
        base_resolution += '_scrambled'

    snippet_image = Image.open(image_path + ".png")
    draw = ImageDraw.Draw(snippet_image)

    [AOIs, _, _] = compute_aois(resolution, snippet, scrambled)

    font = ImageFont.truetype("arial.ttf", 18)
    color = (255, 0, 0)

    for nr, aoi_line in enumerate(AOIs['lines']):
        draw.rectangle(
            (aoi_line['start_x'], aoi_line['start_y'], aoi_line['end_x'], aoi_line['end_y']),
            outline=color,
            width=1
        )

        draw.text(
            (AOIs['base_x'] - AOIs['base_indent_x'] / 1.5, aoi_line['start_y'] + AOIs['base_indent_y'] / 8),
            "L" + str(nr+1),
            fill=color,
            font=font
        )

    font = ImageFont.truetype("arial.ttf", 22)
    color = (0, 255, 0)

    for nr, aoi_block in enumerate(AOIs['blocks']):
        draw.rectangle(
            (aoi_block['start_x'], aoi_block['start_y'], aoi_block['end_x'], aoi_block['end_y']),
            outline=color,
            width=1
        )

        draw.text(
            (AOIs['base_x'] - 1.5 * AOIs['base_indent_x'], aoi_block['start_y'] + (aoi_block['end_y'] - aoi_block['start_y']) / 2),
            "B" + str(nr+1),
            fill=color,
            font=font
        )

    color = (0, 0, 255)
    draw.rectangle(
        (AOIs['answer']['start_x'], AOIs['answer']['start_y'], AOIs['answer']['end_x'], AOIs['answer']['end_y']),
        outline=color,
        width=1
    )

    del draw

    output_file = "output/AoiOverlay/" + resolution + '_' + snippet

    if scrambled:
        output_file += '_scrambled'

    snippet_image.save(output_file + "_AOI.png")


if __name__ == "__main__":
    resolutions = ['1050', '1080', '1200']

    snippets = ['Calculation', 'CheckIfLettersOnly', 'InsertSort', 'MoneyClass', 'Rectangle', 'SignChecker', 'Street', 'Student', 'SumArray', 'Vehicle']
    #snippets = ['Vehicle']

    for resolution in resolutions:
        for snippet in snippets:
            draw_snippet_aoi_overlay(resolution, snippet)
            draw_snippet_aoi_overlay(resolution, snippet, True)

            # todo add exception for the incorrectly scrambled snippet (CheckIfLettersOnly)
            # todo add exception for scrambled rectangle snippet, second result line has an additional "" +
            # todo add exception for vehicle issue
