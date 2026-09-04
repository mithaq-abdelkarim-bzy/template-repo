import * as HX from "hx-model-components";
import { getNodeValue, wrapWith } from "./utilities";

export const coordPropTypes = {
  series: HX.PropTypes.arrayOfType(
    HX.PropTypes.oneOfType([
      HX.PropTypes.objectOfType({
        seriesLabel: HX.PropTypes.string.optional,
        seriesLabelBy: HX.PropTypes.path.optional,
        points: HX.PropTypes.arrayOfType(
          HX.PropTypes.oneOfType([
            HX.PropTypes.objectOfType({
              x: HX.PropTypes.path,
              y: HX.PropTypes.path,
              label: HX.PropTypes.string.optional,
              labelBy: HX.PropTypes.path.optional,
            }),
            HX.PropTypes.objectOfType({
              list: HX.PropTypes.path,
              x: HX.PropTypes.field,
              y: HX.PropTypes.field,
              labelBy: HX.PropTypes.field.optional,
            }),
          ])
        ),
      }),
      HX.PropTypes.objectOfType({
        seriesList: HX.PropTypes.path,
        seriesLabelBy: HX.PropTypes.field.optional,
        points: HX.PropTypes.arrayOfType(
          HX.PropTypes.oneOfType([
            HX.PropTypes.objectOfType({
              x: HX.PropTypes.field,
              y: HX.PropTypes.field,
              label: HX.PropTypes.string.optional,
              labelBy: HX.PropTypes.field.optional,
            }),
            HX.PropTypes.objectOfType({
              list: HX.PropTypes.field,
              x: HX.PropTypes.field,
              y: HX.PropTypes.field,
              labelBy: HX.PropTypes.field.optional,
            }),
          ])
        ),
      }),
    ])
  ),
};

export function getCoordNodes(props) {
  return props.series.map((seriesEntry) =>
    seriesEntry.seriesList
      ? {
        type: "list",
        path: wrapWith(seriesEntry.seriesList, props.with),
        nodes: {
          label: seriesEntry.seriesLabelBy
            ? { type: "static", path: seriesEntry.seriesLabelBy }
            : { type: "const", value: undefined },
          points: seriesEntry.points.map((pointsEntry) =>
            pointsEntry.list
              ? {
                type: "list",
                path: pointsEntry.list,
                nodes: {
                  label: pointsEntry.labelBy
                    ? { type: "static", path: pointsEntry.labelBy }
                    : { type: "const", value: undefined },
                  x: { type: "static", path: pointsEntry.x },
                  y: { type: "static", path: pointsEntry.y },
                },
              }
              : {
                label: pointsEntry.labelBy
                  ? { type: "static", path: pointsEntry.labelBy }
                  : { type: "const", value: pointsEntry.label },
                x: { type: "static", path: pointsEntry.x },
                y: { type: "static", path: pointsEntry.y },
              }
          ),
        },
      }
      : {
        label: seriesEntry.seriesLabelBy
          ? {
            type: "static",
            path: wrapWith(seriesEntry.seriesLabelBy, props.with),
          }
          : { type: "const", value: seriesEntry.seriesLabel },
        points: seriesEntry.points.map((pointsEntry) =>
          pointsEntry.list
            ? {
              type: "list",
              path: wrapWith(pointsEntry.list, props.with),
              nodes: {
                label: pointsEntry.labelBy
                  ? { type: "static", path: pointsEntry.labelBy }
                  : { type: "const", value: undefined },
                x: { type: "static", path: pointsEntry.x },
                y: { type: "static", path: pointsEntry.y },
              },
            }
            : {
              label: pointsEntry.labelBy
                ? {
                  type: "static",
                  path: wrapWith(pointsEntry.labelBy, props.with),
                }
                : { type: "const", value: pointsEntry.label },
              x: {
                type: "static",
                path: wrapWith(pointsEntry.x, props.with),
              },
              y: {
                type: "static",
                path: wrapWith(pointsEntry.y, props.with),
              },
            }
        ),
      }
  );
}

export function getCoordChartData(coordSeriesNodes) {
  return coordSeriesNodes
    .map((entry, seriesIndex) =>
      entry.type === "list"
        ? entry.elements.map(
          (seriesElement) => seriesElement
            ? ({
              label: getNodeValue(seriesElement.nodes.label),
              points: seriesElement.nodes.points
                .map((pointsEntry) =>
                  pointsEntry.type === "list"
                    ? pointsEntry.elements.map(
                      (pointsElement) => pointsElement
                        ? ({
                          label: getNodeValue(pointsElement.nodes.label),
                          x: getNodeValue(pointsElement.nodes.x),
                          y: getNodeValue(pointsElement.nodes.y),
                        })
                        : null
                    ).filter(e => !!e)
                    : [
                      {
                        label: getNodeValue(pointsEntry.label),
                        x: getNodeValue(pointsEntry.x),
                        y: getNodeValue(pointsEntry.y),
                      },
                    ]
                )
                .flat(),
            })
            : null
        ).filter(e => !!e)
        : [
          {
            label:
              getNodeValue(entry.label) ??
              entry.points.metadata?.view?.label ??
              `Series ${seriesIndex}`,
            points: entry.points
              .map((pointsEntry, pointIndex) =>
                pointsEntry.type === "list"
                  ? pointsEntry.elements.map(
                    (element) => element
                      ? ({
                        label: getNodeValue(element.nodes.label),
                        x: getNodeValue(element.nodes.x),
                        y: getNodeValue(element.nodes.y),
                      })
                      : null
                  ).filter(e => !!e)
                  : [
                    {
                      label:
                        getNodeValue(pointsEntry.label) ??
                        pointsEntry.x.metdata.view?.label ??
                        `Point ${pointIndex}`,
                      x: getNodeValue(pointsEntry.x),
                      y: getNodeValue(pointsEntry.y),
                    },
                  ]
              )
              .flat(),
          },
        ]
    )
    .flat();
}