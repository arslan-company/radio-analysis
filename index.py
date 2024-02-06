from dataclasses import dataclass

import streamlit as st

from acr_cloud import broadcast_database


@dataclass
class Response:
    timestamp: str
    duration: str
    title: str
    artist: str
    is_local: bool


def prettier_duration(duration: int) -> str:
    minutes = duration // 60
    seconds = duration % 60
    text = ""
    if minutes > 0:
        text += f"{minutes} dakika "
    if seconds > 0:
        text += f"{seconds} saniye"
    return text.strip()


st.title("Şarkı - Sanatçı Radyo Sayacı")
title_query = st.text_area("Şarkı adı", "")
artist_query = st.text_area("Sanatçı adı", "")

if st.button("Ara"):
    if not title_query.strip() and not artist_query.strip():
        st.error("Lütfen bir değer girin.")
    else:
        try:
            channels = broadcast_database.get_channels()
            responses = {}
            for channel in channels:
                musics = broadcast_database.get_musics(channel.id)
                founds = broadcast_database.search_musics(
                    channel, musics, title_query, artist_query
                )
                for found in founds:
                    if channel.name not in responses:
                        responses[channel.name] = []
                    responses[channel.name].append(
                        Response(
                            found.timestamp,
                            prettier_duration(found.played_duration),
                            found.title,
                            ", ".join([artist for artist in found.artists]),
                            channel.is_local(),
                        )
                    )

            st.write("Şarkı adı için sorgu: ", title_query)
            st.write("Sanatçı adı için sorgu: ", artist_query)
            local_score = 0
            global_score = 0
            for channel, responses in responses.items():
                is_local = responses[0].is_local
                if is_local:
                    local_score += len(responses)
                else:
                    global_score += len(responses)
                st.write(f"Radyo: {channel} {'(Yerel)' if is_local else ''}")
                for response in responses:
                    st.markdown(
                        (
                            f"- {response.timestamp} tarihinde {response.duration} "
                            f"süresince {response.artist} sanatçısının "
                            f"{response.title} şarkısı çalınmıştır.\n"
                        )
                    )
            st.write(
                "Bu sonuçlara göre analiz sonucumuz: "
                f"{local_score + (global_score * 81)}"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
